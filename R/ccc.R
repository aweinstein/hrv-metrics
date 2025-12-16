# Compute Concordance correlation coefficient (CCC) for HRV-rWave data. See
# https://medium.com/@amorimfranchi/concordance-correlation-coefficient-calculation-in-r-98d74ae5f0fc

library(ggplot2)
library(dplyr)
library(patchwork)
library("SimplyAgree")
rm(list = ls()) # Clear the workspace
cat("\014") # Clear the console
while (!is.null(dev.list())) dev.off() # clear all plots

ba_plot <- function(x, y, bias, loa_upper, loa_lower, hrv, detector) {
  m  <- (x + y) / 2
  d  <- x - y
  df <- data.frame(mean = m, diff = d)
  hrv = strsplit(hrv, "_")[[1]][2]
  xlab = sprintf("Average of %s", hrv)
  ylab = sprintf("%s Difference", hrv)
  title = sprintf("Aggreement using %s", detector)
  p = ggplot(df, aes(x = mean, y = diff)) +
    geom_point(alpha = 0.6, size=3) +
    geom_hline(yintercept = bias,      linetype = "solid") +
    geom_hline(yintercept = loa_upper, linetype = "dashed") +
    geom_hline(yintercept = loa_lower, linetype = "dashed") +
    labs(x = xlab, y = ylab, title = title) +
    theme_light() +
    theme(plot.title = element_text(hjust = 0.5, size = 14),
          axis.title = element_text(size = 14),
          axis.text.x = element_text(size = 12),
          axis.text.y = element_text(size = 12))
  
  return(p)
}


make_ba_plots <- function(fn_data, fn_ccc, 
                          setup, skip_methods=c(), skip_experiments=c()) {
  data <- read.csv(fn_data)
  i <- 1
  for (hrv_metric in hrv_metrics) {
    for (experiment_sel in experiments) {
      if (experiment_sel %in% skip_experiments) {next}
      plots = list()
      j = 1
      for (method_sel in methods) {
        if (method_sel %in% skip_methods) {next}
        cat(setup, hrv_metric, experiment_sel, method_sel, "\n")
        df_annotated <- filter(data, method == 'Annotated' & experiment == experiment_sel)
        df_method <- filter(data, method == method_sel & experiment == experiment_sel)
        if (!identical(df_annotated$subject_idx, df_method$subject_idx)) {
          warning("Subjects did do not match")
        }
        a <- df_annotated[[hrv_metric]]
        b <- df_method[[hrv_metric]]
        rst = SimplyAgree::jmvagree(method1=a,
                                    method2=b,
                                    ciWidth=95, agreeWidth=95, CCC=T, plotbland=F)
        df <- data.frame(annotated = df_annotated[[hrv_metric]], 
                         estimated = df_method[[hrv_metric]])
        ba <- agreement_limit(
          x        = "annotated",
          y        = "estimated",
          data     = df,
          loa_calc = "blandaltman"  # classic Bland–Altman method
        )
        bias = rst$blandtab$asDF$estimate[1]
        lower_loa = rst$blandtab$asDF$estimate[2]
        upper_loa = rst$blandtab$asDF$estimate[3]
        p = ba_plot(a, b, ba$loa$bias, ba$loa$lower_loa, ba$loa$upper_loa, 
                    hrv_metric, method_sel)
        plots[[j]] = p
        j <- j + 1
        i <- i + 1
      }
      combined <- wrap_plots(plots, ncol = 4)
      title = sprintf("Bland–Altman plots for setup %s, condition %s and metric %s",
                      setup, experiment_sel, strsplit(hrv_metric, "_")[[1]][2]);
      combined <- combined +
        plot_annotation(title = title) &
        theme(plot.title = element_text(hjust = 0.5))
       
      fn = sprintf("../figures/bland_altman/bland_altman_%s_%s_%s.pdf", 
                   gsub(" ", "_", setup), 
                   experiment_sel, 
                   strsplit(hrv_metric, "_")[[1]][2])
      ggsave(
        fn,
        combined,
        width  = 24,   # in inches
        height = 10,   # increase if labels look tight
        units  = "in",
      )
      print(combined)
    }
  }
}


get_ccc <- function(fn_data, fn_ccc, skip_methods=c(), skip_experiments=c()) {
  data <- read.csv(fn_data)
  ccc_df <- data.frame(method=character(), experiment=character(), 
                       metric=character(), ccc=numeric(), 
                       ccc_lower_ci=numeric(), ccc_upper_ci=numeric(),
                       stringsAsFactors = FALSE)
  i <- 1
  for (method_sel in methods) {
    for (experiment_sel in experiments) {
      if (method_sel %in% skip_methods) {next}
      if (experiment_sel %in% skip_experiments) {next}
      plots = list()
      j = 1
      for (hrv_metric in hrv_metrics) {
        cat(method_sel, experiment_sel, hrv_metric, "\n")
        df_annotated <- filter(data, method == 'Annotated' & experiment == experiment_sel)
        df_method <- filter(data, method == method_sel & experiment == experiment_sel)
        if (!identical(df_annotated$subject_idx, df_method$subject_idx)) {
          warning("Subjects did do not match")
        }
        a <- df_annotated[[hrv_metric]]
        b <- df_method[[hrv_metric]]
        rst = SimplyAgree::jmvagree(method1=a,
                                    method2=b,
                                    ciWidth=95, agreeWidth=95, CCC=T, plotbland=F)
        ccc_df[i, ] <- c(method_sel, experiment_sel, hrv_metric,
                         rst$ccctab$asDF$estimate, rst$ccctab$asDF$lowerci,
                         rst$ccctab$asDF$upperci)
        i <- i + 1
      }
    }
  }
  
  write.csv(ccc_df, fn_ccc, row.names=FALSE)
  cat("CCC data saved in ", fn_ccc, "\n")
  return(data)
}

print("Computing CCC for HRV-rwave data.")

methods <- c("Elgendi_et_al", "Matched_filter", "Wavelet_transform", "Engzee",
             "Christov", "Hamilton", "Pan_Tompkins", "WQRS")
experiments <- c("sitting", "maths", "walking", "hand_bike", "jogging")
hrv_metrics <- c("HRV_MeanNN", "HRV_SDNN", "HRV_RMSSD", "HRV_SDSD", "HRV_CVSD",
                "HRV_CVNN", "HRV_TINN", "HRV_HTI", "HRV_SDRMSSD", "HRV_pNN20",
                "HRV_pNN50", "HRV_IQRNN", "HRV_LF", "HRV_HF",
                "HRV_LFHF", "HRV_LFn", "HRV_HFn", "HRV_LnHF", "HRV_SD1",
                "HRV_SD2", "HRV_SD1SD2", "HRV_SampEn", "HRV_TP")

fn_data <- "../datahrv/chest_strap_setup_subset_HRV_notEngzee.csv"
fn_ccc <- "../datahrv/ccc_chest_strap_df.csv"
data_ein = get_ccc(fn_data, fn_ccc, skip_methods=c("Engzee"))
make_ba_plots(fn_data, fn_ccc, "chest strap", skip_methods=c("Engzee"))

fn_data <- "../datahrv/einthoven_subset_HRV_not_jogging_with_Engzee.csv"
fn_ccc <- "../datahrv/ccc_einthoven_df.csv"
data_ein <- get_ccc(fn_data, fn_ccc, skip_experiments=c("jogging"))
make_ba_plots(fn_data, fn_ccc, "loose cables", skip_experiments=c("jogging"))