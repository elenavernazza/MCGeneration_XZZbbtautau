import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/data_CMS/cms/vernazza/MCProduction/2023_11_14/MyPrivateGridpacks/gg_H_quark-mass-effects_slc7_amd64_gcc700_CMSSW_10_6_37_my_gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M300.tgz'),
    nEvents = cms.untracked.uint32(10000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

# Link to cards:
# https://github.com/elenavernazza/MCGeneration_XZZbbtautau/tree/main/GridpackConfiguration/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M300_NW
#    gg_X_ZZbbtautau_quark-mass-effects_NNPDF30_13TeV.input

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 1',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)


# Link to generator fragment:
# https://raw.githubusercontent.com/cms-sw/genproductions/7d0525c9f6633a9ee00d4e79162d82e369250ccc/python/ThirteenTeV/Hadronizer/Hadronizer_TuneCP5_13TeV_powhegEmissionVeto_1p_LHE_pythia8_cff.py
