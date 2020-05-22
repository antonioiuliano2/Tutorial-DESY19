//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Mar 24 17:17:21 2020 by ROOT version 6.18/04
// from TTree cbmsim//cbmroot
// found on file: ship.conical.PG_11-TGeant4.root
//////////////////////////////////////////////////////////
// Code to read simulation data, first creation 24 March 2020
#ifndef DESY19Sim_h
#define DESY19Sim_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "TClonesArray.h"
#include "TObject.h"
#include "TNamed.h"

class DESY19Sim {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.
   static constexpr Int_t kMaxcbmroot_Stack_MCTrack = 903;
   static constexpr Int_t kMaxcbmroot_EmuDESYTarget_EmuDESYPoint = 1821;
   static constexpr Int_t kMaxcbmroot_SciFiDESY_SciFiDESYPoint = 161;
   static constexpr Int_t kMaxcbmroot_Event_MCEventHeader = 1;

   // Declaration of leaf types
   Int_t           MCTrack_;
   UInt_t          MCTrack_fUniqueID[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   UInt_t          MCTrack_fBits[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Int_t           MCTrack_fPdgCode[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Int_t           MCTrack_fMotherId[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fPx[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fPy[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fPz[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fM[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fStartX[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fStartY[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fStartZ[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fStartT[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Double32_t      MCTrack_fW[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Int_t           MCTrack_fProcID[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Int_t           MCTrack_fNPoints[kMaxcbmroot_Stack_MCTrack];   //[cbmroot.Stack.MCTrack_]
   Int_t           EmuDESYPoint_;
   UInt_t          EmuDESYPoint_fUniqueID[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   UInt_t          EmuDESYPoint_fBits[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Int_t           EmuDESYPoint_fTrackID[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   UInt_t          EmuDESYPoint_fEventId[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fPx[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fPy[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fPz[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fTime[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fLength[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fELoss[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Int_t           EmuDESYPoint_fDetectorID[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fX[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fY[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Double32_t      EmuDESYPoint_fZ[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Int_t           EmuDESYPoint_fPdgCode[kMaxcbmroot_EmuDESYTarget_EmuDESYPoint];   //[cbmroot.EmuDESYTarget.EmuDESYPoint_]
   Int_t           SciFiDESYPoint_;
   UInt_t          SciFiDESYPoint_fUniqueID[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   UInt_t          SciFiDESYPoint_fBits[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Int_t           SciFiDESYPoint_fTrackID[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   UInt_t          SciFiDESYPoint_fEventId[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fPx[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fPy[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fPz[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fTime[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fLength[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fELoss[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Int_t           SciFiDESYPoint_fDetectorID[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fX[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fY[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Double32_t      SciFiDESYPoint_fZ[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   Int_t           SciFiDESYPoint_fPdgCode[kMaxcbmroot_SciFiDESY_SciFiDESYPoint];   //[cbmroot.SciFiDESY.SciFiDESYPoint_]
   //FairMCEventHeader *MCEventHeader_;
   UInt_t          MCEventHeader_TNamed_fUniqueID;
   UInt_t          MCEventHeader_TNamed_fBits;
   TString         MCEventHeader_TNamed_fName;
   TString         MCEventHeader_TNamed_fTitle;
   UInt_t          MCEventHeader_fRunId;
   UInt_t          MCEventHeader_fEventId;
   Double32_t      MCEventHeader_fX;
   Double32_t      MCEventHeader_fY;
   Double32_t      MCEventHeader_fZ;
   Double32_t      MCEventHeader_fT;
   Double32_t      MCEventHeader_fB;
   Int_t           MCEventHeader_fNPrim;
   Bool_t          MCEventHeader_fIsSet;
   Double32_t      MCEventHeader_fRotX;
   Double32_t      MCEventHeader_fRotY;
   Double32_t      MCEventHeader_fRotZ;

   // List of branches
   TBranch        *b_cbmroot_Stack_MCTrack_;   //!
   TBranch        *b_MCTrack_fUniqueID;   //!
   TBranch        *b_MCTrack_fBits;   //!
   TBranch        *b_MCTrack_fPdgCode;   //!
   TBranch        *b_MCTrack_fMotherId;   //!
   TBranch        *b_MCTrack_fPx;   //!
   TBranch        *b_MCTrack_fPy;   //!
   TBranch        *b_MCTrack_fPz;   //!
   TBranch        *b_MCTrack_fM;   //!
   TBranch        *b_MCTrack_fStartX;   //!
   TBranch        *b_MCTrack_fStartY;   //!
   TBranch        *b_MCTrack_fStartZ;   //!
   TBranch        *b_MCTrack_fStartT;   //!
   TBranch        *b_MCTrack_fW;   //!
   TBranch        *b_MCTrack_fProcID;   //!
   TBranch        *b_MCTrack_fNPoints;   //!
   TBranch        *b_cbmroot_EmuDESYTarget_EmuDESYPoint_;   //!
   TBranch        *b_EmuDESYPoint_fUniqueID;   //!
   TBranch        *b_EmuDESYPoint_fBits;   //!
   TBranch        *b_EmuDESYPoint_fTrackID;   //!
   TBranch        *b_EmuDESYPoint_fEventId;   //!
   TBranch        *b_EmuDESYPoint_fPx;   //!
   TBranch        *b_EmuDESYPoint_fPy;   //!
   TBranch        *b_EmuDESYPoint_fPz;   //!
   TBranch        *b_EmuDESYPoint_fTime;   //!
   TBranch        *b_EmuDESYPoint_fLength;   //!
   TBranch        *b_EmuDESYPoint_fELoss;   //!
   TBranch        *b_EmuDESYPoint_fDetectorID;   //!
   TBranch        *b_EmuDESYPoint_fX;   //!
   TBranch        *b_EmuDESYPoint_fY;   //!
   TBranch        *b_EmuDESYPoint_fZ;   //!
   TBranch        *b_EmuDESYPoint_fPdgCode;   //!
   TBranch        *b_cbmroot_SciFiDESY_SciFiDESYPoint_;   //!
   TBranch        *b_SciFiDESYPoint_fUniqueID;   //!
   TBranch        *b_SciFiDESYPoint_fBits;   //!
   TBranch        *b_SciFiDESYPoint_fTrackID;   //!
   TBranch        *b_SciFiDESYPoint_fEventId;   //!
   TBranch        *b_SciFiDESYPoint_fPx;   //!
   TBranch        *b_SciFiDESYPoint_fPy;   //!
   TBranch        *b_SciFiDESYPoint_fPz;   //!
   TBranch        *b_SciFiDESYPoint_fTime;   //!
   TBranch        *b_SciFiDESYPoint_fLength;   //!
   TBranch        *b_SciFiDESYPoint_fELoss;   //!
   TBranch        *b_SciFiDESYPoint_fDetectorID;   //!
   TBranch        *b_SciFiDESYPoint_fX;   //!
   TBranch        *b_SciFiDESYPoint_fY;   //!
   TBranch        *b_SciFiDESYPoint_fZ;   //!
   TBranch        *b_SciFiDESYPoint_fPdgCode;   //!
   TBranch        *b_cbmroot_Event_MCEventHeader_;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fUniqueID;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fBits;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fName;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fTitle;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fRunId;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fEventId;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fX;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fY;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fZ;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fT;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fB;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fNPrim;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fIsSet;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotX;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotY;   //!
   TBranch        *b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotZ;   //!

   DESY19Sim(TTree *tree=0);
   virtual ~DESY19Sim();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef DESY19Sim_cxx
DESY19Sim::DESY19Sim(TTree *tree) : fChain(0) 
{
   string filepath = "../RUN1_sim/ship.conical.PG_11-TGeant4.root";
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject(filepath.data());
      if (!f || !f->IsOpen()) {
         f = new TFile(filepath.data());
      }
      f->GetObject("cbmsim",tree);

   }
   Init(tree);
}

DESY19Sim::~DESY19Sim()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t DESY19Sim::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t DESY19Sim::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void DESY19Sim::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   //MCEventHeader_ = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("MCTrack", &MCTrack_, &b_cbmroot_Stack_MCTrack_);
   fChain->SetBranchAddress("MCTrack.fUniqueID", MCTrack_fUniqueID, &b_MCTrack_fUniqueID);
   fChain->SetBranchAddress("MCTrack.fBits", MCTrack_fBits, &b_MCTrack_fBits);
   fChain->SetBranchAddress("MCTrack.fPdgCode", MCTrack_fPdgCode, &b_MCTrack_fPdgCode);
   fChain->SetBranchAddress("MCTrack.fMotherId", MCTrack_fMotherId, &b_MCTrack_fMotherId);
   fChain->SetBranchAddress("MCTrack.fPx", MCTrack_fPx, &b_MCTrack_fPx);
   fChain->SetBranchAddress("MCTrack.fPy", MCTrack_fPy, &b_MCTrack_fPy);
   fChain->SetBranchAddress("MCTrack.fPz", MCTrack_fPz, &b_MCTrack_fPz);
   fChain->SetBranchAddress("MCTrack.fM", MCTrack_fM, &b_MCTrack_fM);
   fChain->SetBranchAddress("MCTrack.fStartX", MCTrack_fStartX, &b_MCTrack_fStartX);
   fChain->SetBranchAddress("MCTrack.fStartY", MCTrack_fStartY, &b_MCTrack_fStartY);
   fChain->SetBranchAddress("MCTrack.fStartZ", MCTrack_fStartZ, &b_MCTrack_fStartZ);
   fChain->SetBranchAddress("MCTrack.fStartT", MCTrack_fStartT, &b_MCTrack_fStartT);
   fChain->SetBranchAddress("MCTrack.fW", MCTrack_fW, &b_MCTrack_fW);
   fChain->SetBranchAddress("MCTrack.fProcID", MCTrack_fProcID, &b_MCTrack_fProcID);
   fChain->SetBranchAddress("MCTrack.fNPoints", MCTrack_fNPoints, &b_MCTrack_fNPoints);
   fChain->SetBranchAddress("EmuDESYPoint", &EmuDESYPoint_, &b_cbmroot_EmuDESYTarget_EmuDESYPoint_);
   fChain->SetBranchAddress("EmuDESYPoint.fUniqueID", EmuDESYPoint_fUniqueID, &b_EmuDESYPoint_fUniqueID);
   fChain->SetBranchAddress("EmuDESYPoint.fBits", EmuDESYPoint_fBits, &b_EmuDESYPoint_fBits);
   fChain->SetBranchAddress("EmuDESYPoint.fTrackID", EmuDESYPoint_fTrackID, &b_EmuDESYPoint_fTrackID);
   fChain->SetBranchAddress("EmuDESYPoint.fEventId", EmuDESYPoint_fEventId, &b_EmuDESYPoint_fEventId);
   fChain->SetBranchAddress("EmuDESYPoint.fPx", EmuDESYPoint_fPx, &b_EmuDESYPoint_fPx);
   fChain->SetBranchAddress("EmuDESYPoint.fPy", EmuDESYPoint_fPy, &b_EmuDESYPoint_fPy);
   fChain->SetBranchAddress("EmuDESYPoint.fPz", EmuDESYPoint_fPz, &b_EmuDESYPoint_fPz);
   fChain->SetBranchAddress("EmuDESYPoint.fTime", EmuDESYPoint_fTime, &b_EmuDESYPoint_fTime);
   fChain->SetBranchAddress("EmuDESYPoint.fLength", EmuDESYPoint_fLength, &b_EmuDESYPoint_fLength);
   fChain->SetBranchAddress("EmuDESYPoint.fELoss", EmuDESYPoint_fELoss, &b_EmuDESYPoint_fELoss);
   fChain->SetBranchAddress("EmuDESYPoint.fDetectorID", EmuDESYPoint_fDetectorID, &b_EmuDESYPoint_fDetectorID);
   fChain->SetBranchAddress("EmuDESYPoint.fX", EmuDESYPoint_fX, &b_EmuDESYPoint_fX);
   fChain->SetBranchAddress("EmuDESYPoint.fY", EmuDESYPoint_fY, &b_EmuDESYPoint_fY);
   fChain->SetBranchAddress("EmuDESYPoint.fZ", EmuDESYPoint_fZ, &b_EmuDESYPoint_fZ);
   fChain->SetBranchAddress("EmuDESYPoint.fPdgCode", EmuDESYPoint_fPdgCode, &b_EmuDESYPoint_fPdgCode);
   fChain->SetBranchAddress("SciFiDESYPoint", &SciFiDESYPoint_, &b_cbmroot_SciFiDESY_SciFiDESYPoint_);
   fChain->SetBranchAddress("SciFiDESYPoint.fUniqueID", SciFiDESYPoint_fUniqueID, &b_SciFiDESYPoint_fUniqueID);
   fChain->SetBranchAddress("SciFiDESYPoint.fBits", SciFiDESYPoint_fBits, &b_SciFiDESYPoint_fBits);
   fChain->SetBranchAddress("SciFiDESYPoint.fTrackID", SciFiDESYPoint_fTrackID, &b_SciFiDESYPoint_fTrackID);
   fChain->SetBranchAddress("SciFiDESYPoint.fEventId", SciFiDESYPoint_fEventId, &b_SciFiDESYPoint_fEventId);
   fChain->SetBranchAddress("SciFiDESYPoint.fPx", SciFiDESYPoint_fPx, &b_SciFiDESYPoint_fPx);
   fChain->SetBranchAddress("SciFiDESYPoint.fPy", SciFiDESYPoint_fPy, &b_SciFiDESYPoint_fPy);
   fChain->SetBranchAddress("SciFiDESYPoint.fPz", SciFiDESYPoint_fPz, &b_SciFiDESYPoint_fPz);
   fChain->SetBranchAddress("SciFiDESYPoint.fTime", SciFiDESYPoint_fTime, &b_SciFiDESYPoint_fTime);
   fChain->SetBranchAddress("SciFiDESYPoint.fLength", SciFiDESYPoint_fLength, &b_SciFiDESYPoint_fLength);
   fChain->SetBranchAddress("SciFiDESYPoint.fELoss", SciFiDESYPoint_fELoss, &b_SciFiDESYPoint_fELoss);
   fChain->SetBranchAddress("SciFiDESYPoint.fDetectorID", SciFiDESYPoint_fDetectorID, &b_SciFiDESYPoint_fDetectorID);
   fChain->SetBranchAddress("SciFiDESYPoint.fX", SciFiDESYPoint_fX, &b_SciFiDESYPoint_fX);
   fChain->SetBranchAddress("SciFiDESYPoint.fY", SciFiDESYPoint_fY, &b_SciFiDESYPoint_fY);
   fChain->SetBranchAddress("SciFiDESYPoint.fZ", SciFiDESYPoint_fZ, &b_SciFiDESYPoint_fZ);
   fChain->SetBranchAddress("SciFiDESYPoint.fPdgCode", SciFiDESYPoint_fPdgCode, &b_SciFiDESYPoint_fPdgCode);
  // fChain->SetBranchAddress("MCEventHeader.", &MCEventHeader_, &b_cbmroot_Event_MCEventHeader_);
   fChain->SetBranchAddress("MCEventHeader.TNamed.fUniqueID", &MCEventHeader_TNamed_fUniqueID, &b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fUniqueID);
   fChain->SetBranchAddress("MCEventHeader.TNamed.fBits", &MCEventHeader_TNamed_fBits, &b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fBits);
   fChain->SetBranchAddress("MCEventHeader.TNamed.fName", &MCEventHeader_TNamed_fName, &b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fName);
   fChain->SetBranchAddress("MCEventHeader.TNamed.fTitle", &MCEventHeader_TNamed_fTitle, &b_MCEventHeader_cbmroot_Event_MCEventHeader_TNamed_fTitle);
   fChain->SetBranchAddress("MCEventHeader.fRunId", &MCEventHeader_fRunId, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fRunId);
   fChain->SetBranchAddress("MCEventHeader.fEventId", &MCEventHeader_fEventId, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fEventId);
   fChain->SetBranchAddress("MCEventHeader.fX", &MCEventHeader_fX, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fX);
   fChain->SetBranchAddress("MCEventHeader.fY", &MCEventHeader_fY, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fY);
   fChain->SetBranchAddress("MCEventHeader.fZ", &MCEventHeader_fZ, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fZ);
   fChain->SetBranchAddress("MCEventHeader.fT", &MCEventHeader_fT, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fT);
   fChain->SetBranchAddress("MCEventHeader.fB", &MCEventHeader_fB, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fB);
   fChain->SetBranchAddress("MCEventHeader.fNPrim", &MCEventHeader_fNPrim, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fNPrim);
   fChain->SetBranchAddress("MCEventHeader.fIsSet", &MCEventHeader_fIsSet, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fIsSet);
   fChain->SetBranchAddress("MCEventHeader.fRotX", &MCEventHeader_fRotX, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotX);
   fChain->SetBranchAddress("MCEventHeader.fRotY", &MCEventHeader_fRotY, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotY);
   fChain->SetBranchAddress("MCEventHeader.fRotZ", &MCEventHeader_fRotZ, &b_MCEventHeader_cbmroot_Event_MCEventHeader_fRotZ);
   Notify();
}

Bool_t DESY19Sim::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void DESY19Sim::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t DESY19Sim::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef DESY19Sim_cxx
