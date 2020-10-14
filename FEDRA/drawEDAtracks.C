void drawEDAtracks(){
 //which tracks do you want to draw?

//getting tracks set from file
 EdbEDA* gEDA = new EdbEDA("linked_tracks.root",-1,"s[0].Plate()<4&&s[0].Theta()<0.05", kFALSE);
 
 EdbEDATrackSet *set = gEDA->GetTrackSet("TS"); 

// color selection
 //set->SetColorMode(kCOLOR_BY_ID);

 //coloring differently track starting at plate 2 or 3
 int ntracks = set->N();
 for (int itrk = 0; itrk < ntracks; itrk++){
     EdbTrackP *track = set->GetTrack(itrk);
     int color = -1;
     if (track->GetSegmentFirst()->Plate()==1) color = kRed;
     else if (track->GetSegmentFirst()->Plate()==2) color = kGreen;
     else  if (track->GetSegmentFirst()->Plate()==3) color = kBlue;
     //loop on segments
     for (int iseg = 0; iseg < track->N();iseg++) track->GetSegment(iseg)->SetFlag(color);
 }
 set->SetColorMode(kCOLOR_BY_PARTICLE);
 gEDA->Run();


} 