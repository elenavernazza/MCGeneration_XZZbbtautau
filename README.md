# MCGeneration_XZZbbtautau

Let's suppose you need to produce MC samples for your analysis and you don't know how to do it. You are in the right place!
This is an amazing guide to MC production from the very start to the very end.

### Introduction

This guide is divied into two main parts: 
- [How to produce a Gridpack](#1-how-to-produce-a-gridpack)
- [How to generate NanoAOD samples](#2-how-to-generate-miniaodnanoaod-samples)

These two steps are consecutive and it's not possible to generate NanoAOD samples without a gridpack.
In case you already have a reference for central MC production of the same process, you can use the already existing gridpack: in the first part you will find instructions to access the gridpack starting from the central sample.
Once your gridpack is ready, follow the instructions in the second part to generate MiniAOD/NanoAOD ntuples.

# 1. How to produce a Gridpack

## Get the gridpack from a central MC sample

In case you have a central MC sample already existing, or a similar one, you first need to access the gridpack corresponding to the sample.
In this guide we want to generate the process `X->ZZ->bbtautau` starting from the central MC samples `X->ZZ->4l`, scanning different masses of the X resonance.
The reference MC sample name is:

```/GluGluHToZZTo4L_M250_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM```

Some information regarding the dataset can be found on [CMSDAS](https://cmsweb.cern.ch/das/), but we need to access higher level information stored inside the generation fragment.
1. Go to the [McM](https://cms-pdmv-prod.web.cern.ch/mcm/) website and select the request search *"..by dataset name"*: there you need to insert the first part of your MC sample name (e.g. `GluGluHToZZTo4L_M250_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8`) without any `\`. Click on the search button.
2. You will find a list of MC samples with different "PrepId" corresponding to various steps of the MC production (from LHEGEN to NanoAOD). 
3. Click on *"Select View"* and select display of "Fragment" and "Fragment tag". This will show two additional columns that are empty for most of the samples. If you scroll down a bit, you will see two buttons corresponding to the LHEGEN line. 
4. Click on the second button ("Open fragment in a new tab") and you will get the generation fragment, which should look like [this one](https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer20UL16wmLHEGEN-00102/0).

The gridpack used to produce the MC sample is saved in the "args" option and in this example is the following:

```/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_ZZ_NNPDF31_13TeV/gg_H_quark-mass-effects_NNPDF31_13TeV_M250/v3/gg_H_quark-mass-effects_NNPDF31_13TeV_M250.tgz```

The gridpack is usually accessible on lxplus and can be copied to a personal folder. It is a zipped file `*.tgz` if produced with Powheg or `*.tar.xz` if produced with MadGraph.

## Access the information in the gridpack

To access the information stored in the gridpack, you can simply copy the gridpack to a private folder and unzip it.

```
ssh <user>@lxplus.cern.ch
mkdir gg_H_quark-mass-effects_NNPDF31_13TeV_M250
cd gg_H_quark-mass-effects_NNPDF31_13TeV_M250
cp /cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_ZZ_NNPDF31_13TeV/gg_H_quark-mass-effects_NNPDF31_13TeV_M250/v3/gg_H_quark-mass-effects_NNPDF31_13TeV_M250.tgz .
tar xvf gg_H_quark-mass-effects_NNPDF31_13TeV_M250.tgz
```

This will extract all the files contained in the gridpack. In particular, one might be interested in the configuration of the process, which is stored in different locations according to the generator used.

**Powheg**: 
- The `powheg.input` stores the configuration for the first part of the process (e.g. the production of the X resonance).
- The `JHUGen.input` stores the configuration for the decay part of the process (e.g. the X particle decaying to ZZ and then to bbtautau).

**Madgraph**: 
- The `InputCards` folder contains different files defining the process (`*proc_card.dat`), the configuration (`*_run_card.dat`) and the models used (`*_extramodels.dat`).

## Create your own gridpack

You can take these configuration files as starting point and modify some details to create your own gridpack (make sure the parameters are well set by following the instructions or asking the MC contacts).
Once your configuration is ready,
- follow [this guide](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PowhegBOXPrecompiled#Gridpack_production_in_three_ste) if you wish to produce girdpacks with Powheg,
- follow [this guide](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO) if you wish to produce gridpacks with MadGraph.

<details>
<summary>My private gridpack production</summary>

```
cd /data_CMS/cms/vernazza/MCProduction/2023_11_14/GridpackProduction/
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_37
cd CMSSW_10_6_37/src/
cmsenv
```

```
git clone -b powhegUL https://github.com/cms-sw/genproductions.git genproductions
cd genproductions/bin/Powheg/
mkdir gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW
```

Take the reference `powheg.input` and change PDFs (`325300`), mass (`hmass`) and width (`hwidth`) values.
Take the reference `JHUGen.input` and put everywhere
```DecayMode1=2 DecayMode2=-289 ReweightDecay WidthSchemeIn=3 ReadPMZZ```.

The manual for JHU can be found [here](https://spin.pha.jhu.edu/Manual.pdf).

```
cp powheg.input gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW/gg_X_ZZbbtautau_quark-mass-effects_NNPDF30_13TeV.input
cp JHUGen.input gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW/JHUGen.input
```

Before compiling, choose the correct model name in [this page](https://powhegbox.mib.infn.it/#NLOps): in our case it is `gg_H_quark-mass-effects`.

1. Compile:
```
python ./run_pwg_condor.py -p 0 -i gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW/gg_X_ZZbbtautau_quark-mass-effects_NNPDF30_13TeV.input -m gg_H_quark-mass-effects -f my_gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW
```
2. Run (the number of events should be the same number you want to generate in the end):
```
python ./run_pwg_condor.py -p 123 -i gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW/gg_X_ZZbbtautau_quark-mass-effects_NNPDF30_13TeV.input -m gg_H_quark-mass-effects -f my_gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW -q tomorrow -n 100000
```
3. Compress:
```
python ./run_pwg_condor.py -p 9 -i gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW/gg_X_ZZbbtautau_quark-mass-effects_NNPDF30_13TeV.input -m gg_H_quark-mass-effects -f my_gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW -k 1
```
This will generate the gridpack: `gg_H_quark-mass-effects_slc7_amd64_gcc10__my_gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M200_NW.tgz`

For the already existing configuration:
```
cd /data_CMS/cms/vernazza/MCProduction/2023_11_14/GridpackProduction/
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_37
cd CMSSW_10_6_37/src/
cmsenv
git clone -b powhegUL https://github.com/cms-sw/genproductions.git genproductions
cd genproductions/bin/Powheg/
git clone git@github.com:elenavernazza/MCGeneration_XZZbbtautau.git
cp -r  MCGeneration_XZZbbtautau/GridpackConfiguration/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M* .
```

Run all the commands in the `MCGeneration_XZZbbtautau/GridpackConfiguration/Instructions.sh` file.

</details>

<br />

# 2. How to generate MiniAOD/NanoAOD samples

**Note**: From now on, it is very important to set the right CMSSW release for each step of the production. If you have a reference central MC sample, use **the same configuration**.

The following paragraph will guide you in finding the same CMSSW release and commands used centrally.

## How to find the CMSSW release used centrally

The MiniAOD/NanoAOD samples are produced centrally with a chain of steps going from the generator level to the full reconstruction of CMS.
The configuration for each step can be found in web-pages similar to [this one](https://cmsweb.cern.ch/reqmgr2/fetch?rid=cmsunified_ACDC0_task_HIG-RunIISummer20UL18wmLHEGEN-00060__v1_T_201202_125554_3103).
You generally have two ways to access this page for your central MC sample:
- On [CMSDAS](https://cmsweb.cern.ch/das/):
1. Search your MC dataset sample
2. Click on *"Configs"* and then on *"ReqMgr info"*.
Sometimes this link is broken.
- On [McM](https://cms-pdmv-prod.web.cern.ch/mcm/):
1. Search your MC dataset sample (type only the first part of the name, without `\`)
2. Click on the camera symbol (last one) and then on *"ReqMgr"*.

In the ReqMgr page you can see the configuration files used for each step of the production.
By clicking on a file, you will open a configuration like [this one](https://cmsweb.cern.ch/couchdb/reqmgr_config_cache/0fea6eb73257da6a2127ea3c5602dc07/configFile) where you can find the command to generate the same configuration under *"# with command line options:"*.

In the ReqMgr page you can click on "JSON" to display the elist of steps with the corresponding "CMSSWVersion" used.

For each step, we will reproduce the same command in the same CMSSW release (here we use generally CMSSW_X_Y_Z).

## Step 0

In case you want to generate MiniAOD/NanoAOD samples and you don't have a gridpack already, follow the previous step on [how to produce a gridpack](#1-how-to-produce-a-gridpack).

In case you already have a gridpack, the first step to have your ntuples is to create a new fragment.
You can start from the same fragment associated to a central MC sample. In case you don't know how to get a fragment, follow the steps 1-4 described above in [this section](#get-the-gridpack-from-a-central-mc-sample).

Produce and compile your fragment.

```
cmsrel CMSSW_X_Y_Z
cd CMSSW_X_Y_Z/src/
cmsenv
mkdir -p Configuration/GenProduction/python/
touch Configuration/GenProduction/python/<my_fragment>.py
```

For this example we will use this [fragment](https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer20UL18wmLHEGEN-00060/0). Copy the reference fragment to a private loaction and change the path to your gridpack in the `args` option. In case it's needed, change the number of events `nEvents`.

```
scram b
```

Generate the config file with the same command stored in the central configFile:

```
cmsDrive.py Configuration/GenProduction/python/<my_fragment>.py --python_filename <name>_Step0_cfg.py <other options>
```

In the example, the command will be:

```
cmsDriver.py Configuration/GenProduction/python/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW-fragment.py --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NW_0_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step0/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_LHEGEN.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 100000
```

This will create a `<name>_Step0_cfg.py` file that you can run in the correct CMSSW environment with
```
cmsRun <name>_Step0_cfg.py
```

## Step 1 and following...

Generate the config file with the same command stored in the central configFile:

```
cmsDrive.py step1 --python_filename <name>_Step1_cfg.py <other options>
cmsRun <name>_Step1_cfg.py
```

<details>
<summary>My merged private steps 2018</summary>

**Prepare fragment**
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv
mkdir -p Configuration/GenProduction/python/
touch Configuration/GenProduction/python/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250-fragment.py
scram b
```

**Step 0**
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv

cmsDriver.py Configuration/GenProduction/python/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250-fragment.py \
 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py --eventcontent RAWSIM,LHE \
 --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE \
 --fileout file:TestOut.root \
 --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision \
 --step LHE,GEN --geometry DB:Extended \
 --era Run2_2018 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py
```

**Step 1**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step1 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py \
 --fileout file:TestOut.root \
 --eventcontent RAWSIM --datatier GEN-SIM-DIGI \
 --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX \
 --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision \
 --step SIM,DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 \
 --nThreads 8 --geometry DB:Extended \
 --filein file:TestIn.root \
 --datamix PreMix \
 --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py
```

**Step 2**
```
cmsrel CMSSW_10_2_16_UL
cd CMSSW_10_2_16_UL/src
cmsenv

cmsDriver.py step2 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py \
 --fileout file:TestOut.root \
 --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW \
 --conditions 102X_upgrade2018_realistic_v15 --customise_commands "process.source.bypassVersionCheck = cms.untracked.bool(True)" \
 --step HLT:2018v32 \
 --nThreads 8 --geometry DB:Extended \
 --filein file:TestIn.root \
 --era Run2_2018 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py
```

**Step 3**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step3 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py \
 --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM-MINIAODSIM \
 --fileout file:TestOut.root \
 --conditions 106X_upgrade2018_realistic_v11_L1v1 \
 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT \
 --nThreads 8 --geometry DB:Extended \
 --filein file:TestIn.root \
 --era Run2_2018 --runUnscheduled --no_exec --mc -n 5

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py
```

**Step 4**
```
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv

cmsDriver.py step4 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4_cfg.py \
 --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM \
 --fileout file:TestOut.root \
 --conditions 106X_upgrade2018_realistic_v15_L1v1 \
 --step NANO --nThreads 8 \
 --filein file:TestIn.root \
 --era Run2_2018,run2_nanoAOD_106Xv1 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4_cfg.py
```

</details>

<details>
<summary>My original private steps 2018</summary>

**Prepare fragment**
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv
mkdir -p Configuration/GenProduction/python/
touch Configuration/GenProduction/python/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250-fragment.py
scram b
```

**Step 0**
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv

cmsDriver.py Configuration/GenProduction/python/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250-fragment.py --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step0/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_LHEGEN.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py
```

**Step 1**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step1 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step1/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_SIM.root  --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --nThreads 8 --geometry DB:Extended --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step0/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_LHEGEN.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_1_cfg.py
```

**Step 2**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step2 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step2/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_DIGI.root --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step1/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_SIM.root --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

voms
cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_2_cfg.py
```

**Step 3**
```
cmsrel CMSSW_10_2_16_UL
cd CMSSW_10_2_16_UL/src
cmsenv

cmsDriver.py step3 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step3/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_HLT.root  --conditions 102X_upgrade2018_realistic_v15 --customise_commands "process.source.bypassVersionCheck = cms.untracked.bool(True)" --step HLT:2018v32 --nThreads 8 --geometry DB:Extended --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step2/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_DIGI.root  --era Run2_2018 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_3_cfg.py
```

**Step 4**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step4 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step4/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_RECO.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --nThreads 8 --geometry DB:Extended --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step3/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_HLT.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_4_cfg.py
```

**Step 5**
```
cmsrel CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
cmsenv

cmsDriver.py step5 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_5_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step5/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_MINI.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step PAT --nThreads 8 --geometry DB:Extended --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step4/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_RECO.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_5_cfg.py
```

**Step 6**
```
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv

cmsDriver.py step6 --python_filename gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_6_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step6/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_NANOAODv2.root --conditions 106X_upgrade2018_realistic_v15_L1v1 --step NANO --nThreads 8 --filein file:/data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/Step5/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_MINI.root --era Run2_2018,run2_nanoAOD_106Xv1 --no_exec --mc -n 50

cmsRun gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_6_cfg.py
```

</details>