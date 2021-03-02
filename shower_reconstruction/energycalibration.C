//check molteplicity of reconstructed sim showers
vector<double> eff_formula(int found, int total){
  vector<double> efficiency; //value and error
  
  efficiency.push_back((double) found/total);
  double efferr = TMath::Sqrt(efficiency[0] * (1- efficiency[0])/total);
  efficiency.push_back(efferr);
  
  return efficiency;
  
}
void electronscut(){
  const int nsims = 2;

  const int minsize = 10;
  const int maxsize = 110;
  const int sizestep = 10;
  const int ncuts = (int) (maxsize - minsize)/sizestep;
  int sizecut = minsize;

  TGraphErrors *gcut = new TGraphErrors();

  TString prepath_res = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/";
  TString foldernames[nsims] = {"RUN3_differentenergies_17_December_2020/6GeV","RUN3_differentenergiestest_18_December_2020/6GeV"};
  TString subpath("/b000003/shower1.root");

  TChain *showerchain = new TChain("treebranch");
  //get trees
  for (int isim = 0; isim < nsims; isim++){
  showerchain->Add((prepath_res+foldernames[isim]+subpath).Data());
  }
  //building a dataframe with the chain
  ROOT::RDataFrame df(*showerchain);
  auto nshowers = df.Count();
  for (int icut = 0; icut<ncuts; icut++){
   auto ngoods = df.Filter(Form("sizeb>=%i",sizecut)).Count();
   vector<double> efficiency = eff_formula(*ngoods,*nshowers);
   gcut->SetPoint(icut, sizecut, efficiency[0]);
   gcut->SetPointError(icut,0,efficiency[1]);
   cout<<"At cut "<<sizecut<<"how many shower good ?"<<*ngoods<<" over "<<*nshowers<<" ratio: "<<efficiency[0]<<"pm : "<<efficiency[1]<<endl;
   sizecut = sizecut + sizestep;
  }
  gcut->SetMarkerStyle(kFullCircle);
  gcut->SetMarkerColor(kRed);
  gcut->Draw("AP");

}

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
 TH1D *hres[nenergies];
 for (int ienergy = 0; ienergy < nenergies; ienergy++)
  hres[ienergy] = new TH1D(TString::Format("hres[%i]",ienergy),TString::Format("Energy resolution for energy %i GeV;#DeltaE/E",ienergy+1),30,-1.5,1.5);
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
 int intenergy; //energy approximated to int (lower)

 const int nentriesres = showerchain->GetEntries() - nentriesfit;
 cout<<"TOTAL ENTRIES FOR ESTIMATION OF RESOLUTION"<<nentriesres<<endl;

 //second loop

 for (int ishower = nentriesfit; ishower < (nentriesfit+nentriesres);ishower++){
  showerchain->GetEntry(ishower);
  //if (sizeb > 50 && sizeb < 180) {
  if (sizeb > 50) {
   showerenergy = TMath::Sqrt(P[0]*P[0] + emass * emass);

   Erec = sizeb * slope + intercept;
   Eres = (Erec - showerenergy)/showerenergy;

   int intenergy = TMath::Nint	(showerenergy);
   if (intenergy > 0) intenergy = intenergy - 1; //from 0 to 9, energies from 1 to 10	


   if(intenergy >= 0 && intenergy < 10) hres[intenergy]->Fill(Eres);
   hEtrueErec->Fill(showerenergy,Erec);
  }
 }

 //drawing plots and fitting resolution, producing graph
 TCanvas *cres[nenergies];
 TF1 *gausfit[nenergies];
 TGraphErrors *resgraph = new TGraphErrors();
 for (int ienergy = 0; ienergy < nenergies; ienergy++){
  //defining the function
  gausfit[ienergy] = new TF1(TString::Format("gausfit[%i]",ienergy),"gaus",-1.5,1.5);
  gausfit[ienergy]->SetParameters(0,0.25);

  cres[ienergy] = new TCanvas();
  hres[ienergy]->Draw();
  hres[ienergy]->Fit(gausfit[ienergy]);

  if (hres[ienergy]->GetEntries() > 0){

   //adding fit results to graph
   resgraph->SetPoint(ienergy,ienergy+1,gausfit[ienergy]->GetParameter(2));
   resgraph->SetPointError(ienergy,0,gausfit[ienergy]->GetParError(2));
  }
 }

 TCanvas *c2D = new TCanvas();
 hEtrueErec->Draw("COLZ");

 TCanvas *cgraph = new TCanvas();
 resgraph->SetTitle("Energy resolution vs energy;E[GeV];#DeltaE/E");
 resgraph->Draw("AP*");

 TF1 *resfunction = new TF1("resfunction","sqrt(pow([0]/sqrt(x),2)+pow([1],2))");
 resfunction->SetParameters(0.665,0.014);
 resgraph->Fit(resfunction,"","",3,10);

 gStyle->SetOptFit(1011);

}
