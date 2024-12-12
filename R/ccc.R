# Compute Concordance correlation coefficient (CCC) for HRV-rWave data. See
# https://medium.com/@amorimfranchi/concordance-correlation-coefficient-calculation-in-r-98d74ae5f0fc

library(dplyr)
library("SimplyAgree")
rm(list = ls()) # Clear the workspace
cat("\014") # Clear the console

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

fn_data <- "../datahrv/einhoven_subset_HRV_not_jogging_with_Engzee.csv"
fn_ccc <- "../datahrv/ccc_einhoven_df.csv"
data_ein <- get_ccc(fn_data, fn_ccc, skip_experiments=c("jogging"))
