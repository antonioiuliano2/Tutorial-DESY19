//check molteplicity of reconstructed sim showers
void energycalibration(){

 const int nenergies = 7;
 float energies[nenergies] = {1,2,3,4,5,6,7};
 const float epsilon = 0.1;

 TString prepath_fit = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_differentenergies_17_December_2020/";
 TString prepath_res = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_differentenergiestest_18_December_2020/";
 TString foldernames[nenergies] = {"1GeV","2GeV","3GeV","4GeV","5GeV","6GeV","7GeV"};
 TString subpath("/b000003/shower1.root");

 TChain *showerchain = new TChain("treebranch");
 //get trees
 for (int ienergy = 0; ienergy < nenergies; ienergy++){
  showerchain->Add((prepath_fit+foldernames[ienergy]+subpath).Data());
 }

 int maxsize = 1000;
 int sizeb;
 float P[maxsize];

 showerchain->SetBranchAddress("sizeb",&sizeb);
 showerchain->SetBranchAddress("ntrace3simub",&P);

 const int nentriesfit = showerchain->GetEntries();
 cout<<"TOTAL ENTRIES FOR FIT"<<nentriesfit<<endl;

for (int ienergy = 0; ienergy < nenergies; ienergy++){
  showerchain->Add((prepath_res+foldernames[ienergy]+subpath).Data());
 }
 
 //profile histogram
 TProfile *shower_Esize = new TProfile("shower_Esize","Calibration of shower energy measurement;P[GeV/c];sizeb",80,0,8,0,200);
 TProfile *shower_sizeE = new TProfile("shower_sizeE","Calibration of shower energy measurement;sizeb;P[GeV/c]",20,0,200,0,8);
 TH1D *hres = new TH1D("hres", "Momentum resolution;#DeltaP/P",20,-1,1);
 TH2D *hPtruePrec = new TH2D("hPtruePrec","Prec vs Ptrue;Ptrue[GeV/c];Prec[GeV/c]", 80,0,8,80,0,8);
 
 //starting loop

 for (int ishower = 0; ishower < nentriesfit;ishower++){
  showerchain->GetEntry(ishower);
  float P_MC = energies[showerchain->GetTreeNumber()]; //true simulated P
  if (P[0] > P_MC - epsilon && sizeb > 29) {
   shower_Esize->Fill(P[0],sizeb);
   shower_sizeE->Fill(sizeb,P[0]);
  }
 }

 gStyle->SetStatX(0.3);
 gStyle->SetStatY(0.9);

 //drawing plots and fit to a pol0
 TCanvas *c = new TCanvas();
 shower_Esize->Draw();

 //drawing plots and fit to a pol0
 TF1 *calfunc = new TF1("calfunc","pol1",30,200);
 TCanvas *c1 = new TCanvas();
 shower_sizeE->Draw();
 shower_sizeE->Fit(calfunc,"","",30,200);

 float intercept = calfunc->GetParameter(0);
 float slope = calfunc->GetParameter(1);
 float Prec, Pres;

 const int nentriesres = showerchain->GetEntries() - nentriesfit;
 cout<<"TOTAL ENTRIES FOR ESTIMATION OF RESOLUTION"<<nentriesres<<endl;

 //second loop

 for (int ishower = nentriesfit; ishower < (nentriesfit+nentriesres);ishower++){
  showerchain->GetEntry(ishower);
  if (sizeb > 29) {
   Prec = sizeb * slope + intercept;
   Pres = (Prec - P[0])/P[0];

   hres->Fill(Pres);
   hPtruePrec->Fill(P[0],Prec);
  }
 }

 //drawing plots and fitting resolution
 TCanvas * cres = new TCanvas();
 hres->Draw();
 hres->Fit("gaus");

 TCanvas *c2D = new TCanvas();
 hPtruePrec->Draw("COLZ");

}
