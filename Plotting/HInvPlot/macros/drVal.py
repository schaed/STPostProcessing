import ROOT
import sys

can = ROOT.TCanvas('stack', 'stack')
leg = ROOT.TLegend(0.55, 0.60, 0.8, 0.8)
leg.SetBorderSize(0)
leg.SetFillColor(0)

f=ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v45Gam/v45AGamSyst/Wg_strong.root')
tree=f.Get('Wg_strongNominal')
h1 = ROOT.TH1F('dr','dr',50,0.0,5.0)
h2 = ROOT.TH1F('dr2','dr2',50,0.0,5.0)
h1pt = ROOT.TH1F('dpt','dpt',50,0.0,150.0)
h2pt = ROOT.TH1F('dpt2','dpt2',50,0.0,150.0)
phvec=ROOT.TVector3()
v1=ROOT. TVector3()
ie=0
print tree.GetEntries()
sys.stdout.flush()
for e in tree:
    ie+=1
    if ie%10000==0:
        print 'Event:',ie
        sys.stdout.flush()
    if (e.runNumber==364224 or e.runNumber==364225 or (e.runNumber>=312508 and e.runNumber<=312519)):
        for iph in range(0,e.truth_ph_pt.size()):
            phvec.SetPtEtaPhi(e.truth_ph_pt[iph], e.truth_ph_eta[iph], e.truth_ph_phi[iph])
            drmin=99.0
            for ij in range(0,e.truth_jet_pt.size()):
                #if e.truth_jet_pt[ij]/1.3<e.truth_ph_pt[iph]:
                #    continue
                v1.SetPtEtaPhi(e.truth_jet_pt[ij], e.truth_jet_eta[ij], e.truth_jet_phi[ij])
                dr = phvec.DeltaR(v1)
                if drmin>dr:
                    drmin=dr
            for ij in range(0,e.truth_mu_pt.size()):
                v1.SetPtEtaPhi(e.truth_mu_pt[ij], e.truth_mu_eta[ij], e.truth_mu_phi[ij])
                dr = phvec.DeltaR(v1)
                if drmin>dr:
                    drmin=dr
            h1.Fill(drmin,e.w*36000.0)
            h1pt.Fill(e.truth_ph_pt[iph]/1.0e3,e.w*36000.0)
    elif e.runNumber==700016 or e.runNumber==700023:
        drmax=-999
        for iph in range(0,e.truth_ph_pt.size()):
            h2pt.Fill(e.truth_ph_pt[iph]/1.0e3,e.w*36000.0)            
            if e.truth_ph_pt[iph]<15e3:
                continue;
            phvec.SetPtEtaPhi(e.truth_ph_pt[iph], e.truth_ph_eta[iph], e.truth_ph_phi[iph])
            drmin=99.0
            for ij in range(0,e.truth_jet_pt.size()):
                if e.truth_jet_pt[ij]/1.3<e.truth_ph_pt[iph] or e.truth_jet_pt[ij]<30.0e3:
                #if  e.truth_jet_pt[ij]<20.0e3:
                    continue
                v1.SetPtEtaPhi(e.truth_jet_pt[ij], e.truth_jet_eta[ij], e.truth_jet_phi[ij])
                dr = phvec.DeltaR(v1)
                if drmin>dr:
                    drmin=dr
            for ij in range(0,e.truth_mu_pt.size()):
                v1.SetPtEtaPhi(e.truth_mu_pt[ij], e.truth_mu_eta[ij], e.truth_mu_phi[ij])
                dr = phvec.DeltaR(v1)
                if drmin>dr:
                    drmin=dr
            if drmin<99.0 and drmin>drmax:
                drmax=drmin
        h2.Fill(drmax,e.w*36000.0)
can.cd()
h2.GetXaxis().SetTitle('Min #Delta R(jet/lepton,photon)')
h2.GetYaxis().SetTitle('Events')
h2.SetStats(0)
h1.SetStats(0)
h1.SetLineColor(1)
h1.SetMarkerColor(1)
h2.SetLineColor(2)
h2.SetMarkerColor(2)
h2.Draw()
h1.Draw('same')
leg.AddEntry(h1,'Inclusive W+jet')
leg.AddEntry(h2,'W#gamma+jet')
print h1.GetEntries(),h2.GetEntries()
leg.Draw()
can.Update()
#can.WaitPrimitive()

h2pt.GetXaxis().SetTitle('Photon p_{T} [GeV]')
h2pt.GetYaxis().SetTitle('Photons')
h2pt.SetStats(0)
h1pt.SetStats(0)
h1pt.SetLineColor(1)
h1pt.SetMarkerColor(1)
h2pt.SetLineColor(2)
h2pt.SetMarkerColor(2)
h2pt.Draw()
h1pt.Draw('same')
leg.Draw()
can.Update()
can.WaitPrimitive()
