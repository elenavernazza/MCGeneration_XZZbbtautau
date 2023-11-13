# Next time it's better to have 100 jobs with 1000 events

Step 0:
config: CMSSW_10_6_18/src/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py 

'''
python3 batchSubmitterMC.py --step 0 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_18 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
python3 batchSubmitterMC.py --step 0 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW_0_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_18 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
'''

Step 1: (1 & 2) ~7 h to 12 h
config: CMSSW_10_6_17_patch1/src/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1plus2_cfg.py 

'''
python3 batchSubmitterMC.py --step 1 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_17_patch1 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
python3 batchSubmitterMC.py --step 1 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_17_patch1 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
'''

# cmsDriver.py gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1plus2_cfg.py \
#  --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_17_patch1/src/test.root \
#  --eventcontent RAWSIM --datatier GEN-SIM-DIGI \
#  --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX \
#  --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision \
#  --step SIM,DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 \
#  --nThreads 8 --geometry DB:Extended \
#  --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW/Step0/Ntuple_0_numEvent5000.root \
#  --datamix PreMix \
#  --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

Step 2: (3) ~30 min
config: CMSSW_10_2_16_UL/src/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py 

'''
python3 batchSubmitterMC.py --step 2 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_2_16_UL \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
python3 batchSubmitterMC.py --step 2 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_2_16_UL \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
'''

Step 3: (4 & 5)
config: CMSSW_10_6_17_patch1/src/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4plus5_cfg.py 

'''
python3 batchSubmitterMC.py --step 3 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_17_patch1 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
python3 batchSubmitterMC.py --step 3 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_17_patch1 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue long --no_exec
'''

# cmsDriver.py step3 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4plus5_cfg.py \
#  --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM-MINIAODSIM \
#  --fileout file:test.root \
#  --conditions 106X_upgrade2018_realistic_v11_L1v1 \
#  --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT \
#  --nThreads 8 --geometry DB:Extended --filein file:/grid_mnt/data__data.polcms/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_2_16_UL/src/test.root \
#  --era Run2_2018 --runUnscheduled --no_exec --mc -n 5

Step 4: (6)
config: CMSSW_10_6_5/src/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_6_cfg.py 

'''
python3 batchSubmitterMC.py --step 4 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_6_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_5 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue short --no_exec
python3 batchSubmitterMC.py --step 4 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_6_cfg.py \
--cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_5 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW \
--maxEvents 5000 --nJobs 20 --start_from 0 --queue short --no_exec
'''
