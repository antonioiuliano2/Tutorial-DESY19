#define DESY19Sim_cxx
#include "DESY19Sim.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void DESY19Sim::Loop()
{
//   In a ROOT session, you can do:
//      root> .L DESY19Sim.C
//      root> DESY19Sim t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   //****QUI POSSIAMO DICHIARARE ISTOGRAMMI O ALTRE VARIABILI PER IL NOSTRO CODICE****//
   //dichiarazione istogrammi
   TH1D *hp = new TH1D("hp","Track Momentum",65,0,6.5);
   TH2D *hpt_p = new TH2D("hpt_p","Hit PT vs P;P[GeV/c];Pt[GeV/c]",650,0,6.5,200,0,2.);
   //dichiarazione variabili
   Double_t track_momentum;
   Double_t hit_momentum, hit_pt;
   Int_t pdgcode;
   TDatabasePDG *pdgdatabase = TDatabasePDG::Instance(); // instanza databasepdg
   //inizio loop sugli eventi
   int npoints = 0;
   const int maxnpoints = 100;
   Double_t xpoint[maxnpoints],ypoint[maxnpoints],zpoint[maxnpoints];
   for (Long64_t jentry=0; jentry<nentries;jentry++) {

      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      //*** DA QUI SI POSSONO INSERIRE LE OPERAZIONI DA FARE*****//      
      if (jentry%1000==0) cout<< "Arrivato all'evento "<<jentry<<endl;
      //inizio ciclo sulle tracce
      for (int itrk = 0; itrk < MCTrack_; itrk++){
         track_momentum = TMath::Sqrt(pow(MCTrack_fPx[itrk],2)+pow(MCTrack_fPy[itrk],2)+pow(MCTrack_fPz[itrk],2));
         hp->Fill(track_momentum);
      } //fine ciclo sulle tracce

      //inizio ciclo sugli hit
      for (int ipoint = 0; ipoint < EmuDESYPoint_; ipoint++){
        //seleziono hit carichi e faccio eventualmente operazioni sugli hit
        pdgcode = EmuDESYPoint_fPdgCode[ipoint];
        if(pdgdatabase->GetParticle(pdgcode)){ //stiamo escludendo particelle non riconosciute (ioni nucleari)
         if (TMath::Abs(pdgdatabase->GetParticle(pdgcode)->Charge()) > 0){
          hit_momentum = TMath::Sqrt(pow(EmuDESYPoint_fPx[ipoint],2)+pow(EmuDESYPoint_fPy[ipoint],2)+pow(EmuDESYPoint_fPz[ipoint],2));
          hit_pt = TMath::Sqrt(pow(EmuDESYPoint_fPx[ipoint],2)+pow(EmuDESYPoint_fPy[ipoint],2));
          hpt_p->Fill(hit_momentum, hit_pt);

          if (jentry==0 && EmuDESYPoint_fTrackID[ipoint] == 0){
             xpoint[npoints] = EmuDESYPoint_fX[ipoint];
             ypoint[npoints] = EmuDESYPoint_fY[ipoint]; 
             zpoint[npoints] = EmuDESYPoint_fZ[ipoint];
             npoints++;
           }
         }
        }        
      } //fine ciclo sugli hit

   }//fine ciclo sugli eventi
   //disegno istogrammi
   hp->GetXaxis()->SetTitle("P[GeV/c]");
   hp->Draw();
   TCanvas *cppt = new TCanvas();
   hpt_p->Draw("COLZ");

   TCanvas *cgraph = new TCanvas();
   cgraph->Divide(1,2);
   cgraph->cd(1);
   TGraph *gyz = new TGraph(npoints, zpoint, ypoint);
   gyz->SetTitle("zy first electron event 0;z[cm];y[cm]");
   gyz->Draw("AP*");
   cgraph->cd(2);
   TGraph *gxz = new TGraph(npoints, zpoint, xpoint);
   gxz->SetTitle("zx first electron event 0;z[cm];y[cm]");
   gxz->Draw("AP*");   
  

}
