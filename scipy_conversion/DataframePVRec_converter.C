EdbPVRec *gAli = new EdbPVRec();

EdbSegP buildsegment(Long64_t ID, Long64_t PID, double x, double y, double z, double TX, double TY, Long64_t MCEvent, Long64_t MCTrack,double P){
    EdbSegP seg(ID, x, y, TX, TY);
    seg.SetZ(z);
    seg.SetPID(PID);
    seg.SetPlate(29-PID); 
    seg.SetMC(MCEvent,MCTrack);
    seg.SetP(P);
    gAli->AddSegment(seg);
    return seg;
}

void DataframePVRec_converter(){
    ROOT::RDataFrame df = ROOT::RDF::MakeCsvDataFrame("RUN3.csv");
    auto colNames = df.GetColumnNames();
    // Print columns' names
    for (auto &&colName : colNames) std::cout << colName << std::endl;

    auto df0 = df.Define("Segment",buildsegment,{"ID","PID","x","y","z","TX","TY","MCEvent","MCTrack","P"});
    df0.Define("SegmentZ","Segment.Z()").Histo1D("SegmentZ")->DrawClone();

}