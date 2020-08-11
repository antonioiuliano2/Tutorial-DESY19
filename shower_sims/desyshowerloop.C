/*simple script to loop over events, MC tracks and hit points
Works without any include, provided that we are in FairShip environment,
just launch root -l simple_loop in the folder with the simulation output*/
void desyshowerloop(TString filename = "ship.conical.PG_11-TGeant4.root"){

 TFile *file = TFile::Open(filename.Data(),"READ"); 
 if (!file) return;
 TTreeReader reader("cbmsim",file);

 TTreeReaderArray<ShipMCTrack> tracks(reader,"MCTrack");
 TTreeReaderArray<EmuDESYPoint> emupoints(reader,"EmuDESYPoint");

 TDatabasePDG *pdg = TDatabasePDG::Instance();

 int nplates = 57;

// cout<<"Number of events"<<reader.GetEntries()<<endl;
 int ientry = 0;
 int pdgcode,plateid;
 double mass, charge,momentum, energy;

 TProfile * hE_pid = new TProfile("hE_pid","Energy vs PID;PID;E[GeV]", nplates,1,nplates+1, 0, 400);
 TH1I *hoccupancy = new TH1I("hoccupancy","Number of particles per plate", nplates,1, nplates+1);
 TH1D *hmaxplate = new TH1D("hmaxplate","plate with maximum number of particles;PID",nplates,1,nplates+1);

 TH1D *hmaxsegments = new TH1D("hmaxsegments","number of segments at maximum;nelectrons",100,0,100);

 TH1D *hconeangle = new TH1D("hconeangle"," Cone opening angle; #Theta [rad] ",200,0.,0.2);
 TH1D *hconeradius = new TH1D("hconeradius"," Transverse distance from the shower origin; #Delta R[#mum]", 300, 0.,3000.);

 const int nevents = reader.GetEntries();
 
 cout<<"Starting loop over "<<nevents<<endl;

 int nelectrons[nplates];
 int maxelectrons;
 int maxplate;

 TVector3 vertexpos, hitpos;
 TVector3 startP;  

 double tranverse_distance;
 double tx,ty;

 const int npoints = 20;

 double displacement_angle;
 double coneangles[npoints];
 double coneradii[npoints];

 //arrays initializations
 coneangles[0] = 0.01;
 coneradii[0] = 100;

 for (int ipoint = 1; ipoint < npoints; ipoint++){
  coneangles[ipoint] = coneangles[ipoint-1]+0.01;
  coneradii[ipoint] = coneradii[ipoint-1]+100;
 }
 cout<<"TEST "<<coneangles[npoints-1]<<endl;
 TH2D *hecoll2D = new TH2D("hecoll2D","Collected electron efficiency;angle[rad];Radius[#mu m]",npoints,coneangles[0],coneangles[npoints-1]+0.01,npoints,coneradii[0],coneradii[npoints-1]+100);

 int nelectronstot = 0;

 TGraph *effgraph = new TGraph();

 for(int ievent = 0; ievent<nevents;ievent++){
     for(int iplate =0; iplate < nplates; iplate++){
      nelectrons[iplate] = 0; //resetting number of electrons;
     }

     reader.SetEntry(ievent);
     //vertex track position and angles
     vertexpos.SetXYZ(tracks[0].GetStartX(),tracks[0].GetStartY(),tracks[0].GetStartZ());
     startP.SetXYZ(tracks[0].GetPx(), tracks[0].GetPy(), tracks[0].GetPz());
   
     //access the hits:    
     for (const EmuDESYPoint& emupoint: emupoints){
         //pdgcode and kinematics

         pdgcode = emupoint.PdgCode();

         momentum = TMath::Sqrt(pow(emupoint.GetPx(),2) + pow(emupoint.GetPy(),2) + pow(emupoint.GetPz(),2));
         tx = emupoint.GetPx()/emupoint.GetPz();
         ty = emupoint.GetPy()/emupoint.GetPz();
 
         plateid = emupoint.GetDetectorID();
         hitpos.SetXYZ(emupoint.GetX(), emupoint.GetY(), emupoint.GetZ());
 
         TVector3 displacement = hitpos - vertexpos; //vettore spostamento;         
         displacement_angle = displacement.Angle(startP);
         tranverse_distance = TMath::Sqrt(pow(displacement.X(),2)+ pow(displacement.Y(),2));

         //checking particle information
         if(pdg->GetParticle(pdgcode)){
          charge = pdg->GetParticle(pdgcode)->Charge();          
          mass = pdg->GetParticle(pdgcode)->Mass();         
          //saving info for electrons and positrons above visibility threshold
          if (TMath::Abs(charge)>0 && momentum > 0.03 && TMath::ATan(TMath::Sqrt(tx*tx+ty*ty))<1.){
          
           hconeangle->Fill(displacement_angle);
           hconeradius->Fill(tranverse_distance *1.e+4);
           //is hit inside cone+cylinder acceptance region
           for(double & maxconeangle: coneangles){ //is hit inside cone?
            for (double & maxconeradius: coneradii){
             if(TMath::Abs(displacement_angle) < maxconeangle && TMath::Abs(tranverse_distance*1.e+4) < maxconeradius ) hecoll2D->Fill(maxconeangle+0.001,maxconeradius+10.);
            }

           }  
           nelectronstot++;
           

           energy = TMath::Sqrt(mass*mass + momentum * momentum);         
           hE_pid->Fill(plateid, energy);
           hoccupancy->Fill(plateid);
           nelectrons[plateid-1]++;

          }
         }
     }//end of hit loop
  maxelectrons = 0;
  for(int iplate =0; iplate < nplates; iplate++){
   if (nelectrons[iplate] > maxelectrons){
     maxelectrons = nelectrons[iplate];
     maxplate = iplate;
   }
  }
  hmaxplate->Fill(maxplate+1);
  hmaxsegments->Fill(maxelectrons);
 } //end of event loop 

 TCanvas *cecoll2D = new TCanvas();
 hecoll2D->Scale(1./nelectronstot);
 gStyle->SetPaintTextFormat("4.2f");
 hecoll2D->Draw("COLZ && TEXT");
/*
 for(int iangle = 0; iangle < nangles; iangle++){
  effgraph->SetPoint(iangle, coneangles[iangle], (double) nincone[iangle]/nelectronstot);
 }
 
 effgraph->SetTitle("Cone angle acceptance;#Theta[rad];eff");
 effgraph->GetYaxis()->SetRangeUser(0.,1.);
 effgraph->SetMarkerColor(kRed);
 effgraph->SetMarkerStyle(8);
 effgraph->Draw("AP");*/

 TCanvas *cCone = new TCanvas();
 cCone->Divide(1,2);
 cCone->cd(1);
 hconeangle->Draw();
 cCone->cd(2);
 hconeradius->Draw();

 
 TCanvas *cE = new TCanvas();

 hE_pid->Draw();
 TCanvas *c_occ = new TCanvas();
 hoccupancy->Scale(1./nevents);
 hoccupancy->Draw();
 
 TCanvas *cmax = new TCanvas();
 cmax->Divide(2,1);
 cmax->cd(1);
 hmaxplate->Draw();
 cmax->cd(2);
 hmaxsegments->Draw();
}
