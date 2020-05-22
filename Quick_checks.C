//linee di codice di esempio per mostrare utili applicazioni di Scan e Draw per ispezionare degli eventi di interesse

void Quick_checks(){

 int nevent = 90; //un evento di interesse
 
 TFile * simfile = TFile::Open("../RUN1_sim/ship.conical.PG_11-TGeant4.root");
 TTree * simtree = (TTree*) simfile->Get("cbmsim");
 //disegno gli hit per quell'evento(i fotoni, corrispondenti a pdg 22, sono esclusi, poiché non riveliamo particelle neutre);
 TCanvas *c = new TCanvas();
 c->Divide(1,2);
 c->cd(1);
 simtree->Draw("EmuDESYPoint.fX:EmuDESYPoint.fZ","EmuDESYPoint.fPdgCode!=22","*",1,nevent);
 c->cd(2);
 simtree->Draw("EmuDESYPoint.fY:EmuDESYPoint.fZ","EmuDESYPoint.fPdgCode!=22","*",1,nevent);


 //stampo alcune informazioni sulla particella
 //nome particella,id della madre, processo che ha originato la particella, tri-impulso
 simtree->Scan("MCTrack.fPdgCode:MCTrack.fMotherId:MCTrack.fProcessId:MCTrack.fPx:MCtrack.fPy:MCTrack.fPz","","",1,nevent); 

}
