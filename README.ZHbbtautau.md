# Generating Zprime->ZH->bbtautau samples
## Madgraph cards
The original Madgraph cards are at [in the genproductions repo](https://github.com/cms-sw/genproductions/tree/7d0b3289f259c976d6a591b5dc40c60ca39460af/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/exo_diboson/Spin-1/Zprime_Zh_Zhadhbb), taken from Zprime_Zh_Zhadhbb. Z decay channel was changed from hadronic to tautau.

### instructions
Clone the genproductions CMS repository (not in a CMSSW release area).
In a working directory, to prepare the cards :
The cards we want are in `genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/exo_diboson/Spin-1`. 
Copy the folder holding the one you want, for example : `cp -r cards/production/2017/13TeV/exo_diboson/Spin-1/Zprime_Zh_Zhadhbb ./Zprime_Zh_Ztautauhbb`
Edit the `*_proc_card.dat` file (e.g. `prime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow_M/Zprime_Zh_Zbbhtautau_narrow_M_proc_card.dat`) and update the process *and the output name*.
Then run the `.sh` script in the folder (e.g. `chmod +x ./Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow.sh; ./Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow.sh` ) to egenrate the cards for the different mass points (edit the script to choose them).

## Making the gridpacks
Copy the folders with the cards into `genproductions/bin/MadGraph5_aMCatNLO`
Then run `./gridpack_generation.sh <NameOfOutputInProcCard> <pathToCardFolder>`


Steps that I ran (you need to ensure that the folder holding the cards is the same as the name of output in the card)
~~~bash
cd ~/bbtautau/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO

cp -r /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpackConfiguration/Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow_M* .
rm -r Zprime_Zh_Zbbhtautau_narrow_M
for card_folder in $(ls -d Zprime_Zh_Zbbhtautau*/); do
# the & runs in background, don't close the shell before everything is done
# ${x::-1} drops the / at the end of the directory
./gridpack_generation.sh ${card_folder::-1} $card_folder
done

cp -r /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpackConfiguration/Zprime_Zh_Ztautauhbb/Zprime_Zh_Ztautauhbb_narrow_M* .
rm -r Zprime_Zh_Ztautauhbb_narrow_M
for card_folder in $(ls -d Zprime_Zh_Ztautauhbb*/); do
./gridpack_generation.sh ${card_folder::-1} $card_folder
done
~~~

TO cleanup : `rm -r Zprime_Zh_Zbbhtautau_narrow_M*/Zprime_*_gridpack`

### Drawing Feynman diagrams
~~~bash
cd genproductions/bin/MadGraph5_aMCatNLO/Zprime_Zh_Ztautauhbb_narrow_M600/Zprime_Zh_Ztautauhbb_narrow_M600_gridpack/work
./MG5_aMC_v2_9_13/bin/mg5_aMC
# inside madgraph shell, copy paste proc_card.dat
display diagrams ./

~~~

## Preparing the CMSSW config files
We are using the flow [B2G-chain_RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-0200](https://cms-pdmv-prod.web.cern.ch/mcm/chained_requests?prepid=B2G-chain_RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-02000&page=0&shown=15)

CMSSW releases are in `/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases`

Getting the fragment : 
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_13_patch1/src
cmsenv
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIFall18wmLHEGS-01094 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py
scram b
~~~


### cmsDriver commands
`cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration`

The following commands were copied from the B2G production, however the nanoAOD version is old (v7) and is weird thus for now we just copy the config fog gg->X->ZZ.

<details>
<summary>Old B2G-copied process</summary>
After each step we edit the configuration file to add the OptionParser

#### Step 0 (LHE,GEN,SIM)
[LHEGS](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIFall18wmLHEGS-01094&page=0&shown=4398046775347) 	CMSSW_10_2_13_patch1 
Raw cmsDriver command : `cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall18wmLHEGS-01094.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 50`

My commands :
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_13_patch1
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py --python_filename gg_Zprime_ZHtautaubb_0_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall18wmLHEGS-01094.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=0 --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 50
~~~

You need to change the line `process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=0` at the very end of the file

#### Step 1 (DIGI,DATAMIX,L1,DIGI2RAW,HLT)
[ B2G-RunIIAutumn18DRPremix-01091 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18DRPremix-01091&page=0&shown=4398046775347) 	CMSSW_10_2_5

Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-01091_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIIAutumn18DRPremix-01091_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:B2G-RunIIFall18wmLHEGS-01094.root --datamix PreMix --era Run2_2018 --no_exec --mc -n $EVENTS`

NB : following commands takes a long time (normal) and needs grid proxy
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIIAutumn18DRPremix-01091_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:B2G-RunIIFall18wmLHEGS-01094.root --datamix PreMix --era Run2_2018 --no_exec --mc -n 50
~~~


#### Step 2 (RAW2DIGI,L1Reco,RECO,RECOSIM,EI)
[ B2G-RunIIAutumn18DRPremix-01091 second part ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18DRPremix-01091&page=0&shown=4398046775347) 	CMSSW_10_2_5

Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-01091_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIIAutumn18DRPremix-01091.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:B2G-RunIIAutumn18DRPremix-01091_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIIAutumn18DRPremix-01091.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:B2G-RunIIAutumn18DRPremix-01091_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 50
~~~

#### Step3 (MINIAODSIM)
[ B2G-RunIIAutumn18MiniAOD-01089 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18MiniAOD-01089&page=0&shown=4398046775347) 	CMSSW_10_2_5


Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18MiniAOD-01089_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIAutumn18MiniAOD-01089.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_3_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIAutumn18MiniAOD-01089.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n 50
~~~


#### Step4 (NANOAODSIM)
[ B2G-RunIIAutumn18NanoAODv7-02003 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18NanoAODv7-02003&page=0&shown=4398046775347) 		
CMSSW_10_2_22


Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18NanoAODv7-02003_1_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02003.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_22
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_4_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02003.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n 50
~~~

</details>

## Running the jobs
### Snippets
~~~bash
# if you just want to check proxy validity
export export X509_USER_PROXY=~/.t3/proxy.cert
voms-proxy-info
# check fot timeleft: xx:xx:xx
~~~

### Testing locally (version 1 pilot)

~~~bash
source /opt/exp_soft/cms/t3/t3setup

mkdir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots

SCRIPT=/home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/batchSubmitterMC_all.py
BASE_DIR=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots

~~~

#### Zh_Zbbhtautau
##### Using B2G-copied config
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Zbbhtautau_M$MASS
cd gg_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_Zprime_ZHtautaubb_*_cfg.py .

python3 $SCRIPT \
--process gg_Zprime_ZHtautaubb \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

##### Using ZZ config
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Zbbhtautau_M$MASS
cd gg_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Ztautauhbb
For now we use the same config files as ZZ, just changing the gridpack
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Ztautauhbb_M$MASS
cd gg_Zh_Ztautauhbb_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau_*_cfg.py .

# same process as Zh_Zbbhtautau for now, but different gridpacj
python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Ztautauhbb_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

### Runs version 1
~~~bash
source /opt/exp_soft/cms/t3/t3setup

mkdir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs

SCRIPT=/home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/batchSubmitterMC_all.py
BASE_DIR=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs

~~~

#### Pilot ZHtautaubb first version
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_X_ZZbbtautau_M$MASS
cd gg_X_ZZbbtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_Zprime_ZHtautaubb_*_cfg.py .

python3 $SCRIPT \
--process gg_Zprime_ZHtautaubb \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 1000 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Zbbhtautau (using ZZ config)
~~~bash
cd $BASE_DIR
MASS=600
mkdir Zprime_Zh_Zbbhtautau_M$MASS
cd Zprime_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpacksZH/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Ztautauhbb (using ZZ config)
~~~bash
cd $BASE_DIR
MASS=600
mkdir Zprime_Zh_Ztautauhbb_M$MASS
cd Zprime_Zh_Ztautauhbb_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpacksZH/Zprime_Zh_Ztautauhbb_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~