//check molteplicity of reconstructed sim showers
void energycalibration(){

 const int nenergies = 10;
 float energies[nenergies] = {1,2,3,4,5,6,7};
 const float epsilon = 0.1;

 TString prepath_fit = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_differentenergies_17_December_2020/";
 TString prepath_res = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_differentenergiestest_18_December_2020/";
 TString foldernames[nenergies] = {"1GeV","2GeV","3GeV","4GeV","5GeV","6GeV","7GeV","8GeV","9GeV","10GeV"};
 TString subpath("/b000003/shower1.root");

 TChain *showerchain = new TChain("treebranch");
 //get trees
 for (int ienergy = 0; ienergy < nenergies; ienergy++){
  showerchain->Add((prepath_fit+foldernames[ienergy]+subpath).Data());
 }

 int maxsize = 1000;
 int sizeb;
 float P[maxsize];
 float emass = 0.00051;
 float showerenergy;

 showerchain->SetBranchAddress("sizeb",&sizeb);
 showerchain->SetBranchAddress("ntrace3simub",&P);

 const int nentriesfit = showerchain->GetEntries();
 cout<<"TOTAL ENTRIES FOR FIT"<<nentriesfit<<endl;

for (int ienergy = 0; ienergy < nenergies; ienergy++){
  showerchain->Add((prepath_res+foldernames[ienergy]+subpath).Data());
 }
 
 //profile histogram
 TProfile *shower_Esize = new TProfile("shower_Esize","Calibration of shower energy measurement;E[GeV];sizeb",100,0,10,0,300);
 TProfile *shower_sizeE = new TProfile("shower_sizeE","Calibration of shower energy measurement;sizeb;E[GeV]",30,0,300,0,10);
 TH1D *hres = new TH1D("hres","Energy resolution;#DeltaE/E",10,-1.05,0.95);
 TH2D *hEtrueErec = new TH2D("hEtrueErec","Erec vs Etrue;Etrue[GeV/c];Erec[GeV/c]", 100,0,10,100,0,10);
 
 //starting loop

 for (int ishower = 0; ishower < nentriesfit;ishower++){
  showerchain->GetEntry(ishower);
  float P_MC = energies[showerchain->GetTreeNumber()]; //true simulated P
  if (P[0] > P_MC - epsilon && sizeb > 29) {
   showerenergy = TMath::Sqrt(P[0] * P[0] + emass * emass);
   shower_Esize->Fill(showerenergy,sizeb);
   shower_sizeE->Fill(sizeb,showerenergy);
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
 shower_sizeE->Fit(calfunc,"","",50,180);

 float intercept = calfunc->GetParameter(0);
 float slope = calfunc->GetParameter(1);
 float Erec, Eres;

 const int nentriesres = showerchain->GetEntries() - nentriesfit;
 cout<<"TOTAL ENTRIES FOR ESTIMATION OF RESOLUTION"<<nentriesres<<endl;

 //second loop

 for (int ishower = nentriesfit; ishower < (nentriesfit+nentriesres);ishower++){
  showerchain->GetEntry(ishower);
  if (sizeb > 50 && sizeb < 180) {
   showerenergy = TMath::Sqrt(P[0]*P[0] + emass * emass);

   Erec = sizeb * slope + intercept;
   Eres = (Erec - showerenergy)/showerenergy;

   hres->Fill(Eres);
   hEtrueErec->Fill(showerenergy,Erec);
  }
 }

 //drawing plots and fitting resolution
 TCanvas * cres = new TCanvas();
 hres->Draw();
 hres->Fit("gaus");

 TCanvas *c2D = new TCanvas();
 hEtrueErec->Draw("COLZ");

}
