//plotting couples occupancy for all available plates for SHIP DESY testbeam (created by Antonio on 2 June 2020)
void compareoccupancy(){
 const int nruns = 9;
 int whichrun[nruns] = {1,2,4,6,5,7,8,8,3};
 int nplates[nruns] = {57,43,15,29,29,19,15,29,29};
 //TCut cut = TCut("1");
 //TCut cut = TCut("eCHI2P<2.5&&s.eW>13&&eN1==1&&eN2==1&&s1.eFlag>=0&&s2.eFlag>=0");
 TCut cut = TCut("eN1==1&&eN2==1&&s1.eFlag>=0&&s2.eFlag>=0");
int ipoint = 0;
 TGraphErrors *graph[nruns];
 for (int irun=0;irun<nruns;irun++){
  graph[irun] = new TGraphErrors();
  for (int iplate=1;iplate<nplates[irun];iplate++){
   TFile *inputfile;

   if (irun == 6){
    if (iplate<10) inputfile = TFile::Open(Form("/ship/DESY2019/RUN8A/b00000%i/p00%i/%i.%i.0.0.cp.root",whichrun[irun],iplate,whichrun[irun],iplate));
    else inputfile = TFile::Open(Form("/ship/DESY2019/RUN8A/b00000%i/p0%i/%i.%i.0.0.cp.root",whichrun[irun],iplate,whichrun[irun],iplate));
   }
   else if(irun == 7){
    if (iplate<10) inputfile = TFile::Open(Form("/ship/DESY2019/RUN8B/b00000%i/p00%i/%i.%i.0.0.cp.root",whichrun[irun],iplate,whichrun[irun],iplate));  
    else inputfile = TFile::Open(Form("/ship/DESY2019/RUN8B/b00000%i/p0%i/%i.%i.0.0.cp.root",whichrun[irun],iplate,whichrun[irun],iplate));
   }
   else if(irun == 8){
    if (iplate<10) inputfile = TFile::Open(Form("/ship/DESY2019/RUN3_ZURICH/b00000%i/p00%i/%i.%i.0.1000.cp.root",1,iplate,1,iplate));  
    else inputfile = TFile::Open(Form("/ship/DESY2019/RUN8B/b00000%i/p0%i/%i.%i.0.1000.cp.root",1,iplate,1,iplate));
   }
   else{
    if (iplate<10) inputfile = TFile::Open(Form("/ship/DESY2019/RUN%i/b00000%i/p00%i/%i.%i.0.0.cp.root",whichrun[irun],whichrun[irun],iplate,whichrun[irun],iplate));
    else inputfile = TFile::Open(Form("/ship/DESY2019/RUN%i/b00000%i/p0%i/%i.%i.0.0.cp.root",whichrun[irun],whichrun[irun],iplate,whichrun[irun],iplate));
   }

   if(!inputfile) continue;
   TTree *couples = (TTree*) inputfile->Get("couples");
  
   int ncouples = couples->GetEntries(cut);

   graph[irun]->SetPoint(ipoint,iplate,ncouples);
   graph[irun]->SetPointError(ipoint,0.5,TMath::Sqrt(ncouples));
   ipoint++;
  }
 }
 TCanvas *c = new TCanvas();
 graph[0]->SetTitle("RUN1, energy 6GeV, 57 plates");
 graph[0]->SetFillColor(kWhite);
 graph[0]->Draw("AP*");
 
 graph[1]->SetFillColor(kWhite);
 graph[1]->SetMarkerColor(kRed);
 graph[1]->SetTitle("RUN2, energy 6GeV, 43 plates");
 graph[1]->Draw("P*");

 graph[2]->SetTitle("RUN4, energy 6GeV, 15 plates");
 graph[2]->SetFillColor(kWhite);
 graph[2]->SetMarkerColor(kGreen);
 graph[2]->Draw("P*");

 graph[3]->SetTitle("RUN6, energy 4GeV, 29 plates");
 graph[3]->SetFillColor(kWhite);
 graph[3]->SetMarkerColor(kYellow);
 graph[3]->Draw("P*");

 graph[4]->SetTitle("RUN5, energy 2 GeV, 29 plates");
 graph[4]->SetFillColor(kWhite);
 graph[4]->SetMarkerColor(kBlue);
 graph[4]->Draw("P*");

 graph[5]->SetTitle("RUN7, energy 6 GeV, 19 plates");
 graph[5]->SetFillColor(kWhite);
 graph[5]->SetMarkerColor(kMagenta);
 graph[5]->Draw("P*");

 graph[6]->SetTitle("RUN8A, energy 6 GeV, 15 plates");
 graph[6]->SetFillColor(kWhite);
 graph[6]->SetMarkerColor(kOrange);
 graph[6]->Draw("P*");

 graph[7]->SetTitle("RUN8B, energy 6 GeV, 29 plates");
 graph[7]->SetFillColor(kWhite);
 graph[7]->SetMarkerColor(kCyan);
 graph[7]->Draw("P*");

 graph[8]->SetTitle("RUN3, energy 6 GeV, 29 plates");
 graph[8]->SetFillColor(kWhite);
 graph[8]->SetMarkerColor(kRed+3);
 graph[8]->Draw("P*");

 c->BuildLegend();
 
 graph[0]->SetTitle("Couples entries for plate;iplate");
 

}
