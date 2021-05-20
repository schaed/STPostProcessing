#!/bin/bash                                                                                                                                                                                                       
#OUTDIRM=/share/t3data2/schae/v32ETight
#OUTDIRM=${1:-v34mc16a}
OUTDIRM=v45EGamSyst

if [ $# -eq 1 ]
  then
    OUTDIRM=$1
    echo "outdirectory set: $OUTDIRM"
fi
if [[ $OUTDIRM == "" ]]; then
    echo "OUTDIRM is empty. exiting"
    echo $?    # Non-zero exit status returned -- command failed to execute.
fi
echo "outdirectory set: $OUTDIRM"
mkdir $OUTDIRM
hadd $OUTDIRM/data.root data*root
#hadd $OUTDIRM/VVV.root VVV*root
#rm VVV*root
#hadd $OUTDIRM/Z_strong_VBFFilt.root Z_strong_VBFFilt*root
hadd $OUTDIRM/Z_strongPTVExt.root Z_strongPTVExt*root
hadd $OUTDIRM/Z_strongExt.root Z_strongExt*root
#hadd $OUTDIRM/Z_strongmVBFFilt.root Z_strongmVBFFilt*root
hadd $OUTDIRM/W_strongExt.root W_strongExt*root
#hadd $OUTDIRM/Z_strong_LowMass.root Z_strong_LowMass*root
rm Z_strong_VBFFilt*root
rm Z_strongPTVExt*root
rm Z_strong_LowMass*root
rm Z_strongExt*root
rm Z_strongmVBFFilt*root
rm W_strongExt*root

hadd $OUTDIRM/VBFHgamdark1250.root VBFHgamdark1250*root
rm VBFHgamdark1250*root
hadd $OUTDIRM/VBFHgamdark1500.root VBFHgamdark1500*root
rm VBFHgamdark1500*root
hadd $OUTDIRM/VBFHgamdark1750.root VBFHgamdark1750*root
rm VBFHgamdark1750*root
hadd $OUTDIRM/VBFHgamdark3000.root VBFHgamdark3000*root
rm VBFHgamdark3000*root
hadd $OUTDIRM/VBFHgamdark2000.root VBFHgamdark2000*root
rm VBFHgamdark2000*root
hadd $OUTDIRM/VBFHgamdark1000.root VBFHgamdark1000*root
rm VBFHgamdark1000*root
hadd $OUTDIRM/VBFH2000.root VBFH2000*root
rm VBFH2000*root
hadd $OUTDIRM/VBFH1000.root VBFH1000*root
rm VBFH1000*root
hadd $OUTDIRM/VBFH3000.root VBFH3000*root
rm VBFH3000*root
hadd $OUTDIRM/VBFH750.root VBFH750*root
rm VBFH750*root
hadd $OUTDIRM/VBFH300.root VBFH300*root
rm VBFH300*root
hadd $OUTDIRM/VBFH100.root VBFH100*root
rm VBFH100*root
hadd $OUTDIRM/VBFH75.root VBFH75*root
rm VBFH75*root
hadd $OUTDIRM/VBFH50.root VBFH50*root
rm VBFH50*root
# now hadd the standard samples
#hadd $OUTDIRM/VV.root VV*root
hadd $OUTDIRM/W_strong.root W_strong*root
hadd $OUTDIRM/Z_strong.root Z_strong*root
hadd $OUTDIRM/W_EWKSh.root W_EWKSh*root
hadd $OUTDIRM/Z_EWKSh.root Z_EWKSh*root
rm W_EWKSh*root
rm Z_EWKSh*root
hadd $OUTDIRM/W_EWK.root W_EWK*root
hadd $OUTDIRM/Z_EWK.root Z_EWK*root
hadd $OUTDIRM/ttbar.root ttbar*root
#hadd $OUTDIRM/QCDw.root QCDw*root
#hadd $OUTDIRM/QCDunw.root QCDunw*root
#hadd signal.root *H125*root
#hadd $OUTDIRM/VBFH125Old.root  VBFH125Old*.root
rm VBFH125Old*.root
hadd $OUTDIRM/VBFH125.root  VBFH125*.root
hadd $OUTDIRM/VBFHgam125Old.root  VBFHgam125*312243.root
rm VBFHgam125*312243.root
hadd $OUTDIRM/VBFHgam125.root  VBFHgam125*.root
hadd $OUTDIRM/VBFHOther.root  VBFHOther*.root
hadd $OUTDIRM/VBFHAltSignal.root  VBFHAltSignal*.root
#hadd $OUTDIRM/ggFH125Old.root  ggFH125Old*.root
rm ggFH125Old*.root
hadd $OUTDIRM/ggFH125.root  ggFH125*.root
#hadd $OUTDIRM/VH125Old.root  VH125Old*.root
rm  VH125Old*.root
hadd $OUTDIRM/VH125.root  VH125*.root
hadd $OUTDIRM/TTH125.root  TTH125*.root

hadd $OUTDIRM/Zg_EWK.root  Zg_EWK*.root
hadd $OUTDIRM/Wg_EWK.root  Wg_EWK*.root

hadd $OUTDIRM/Wg_strong222.root Wg_strong222*root
hadd $OUTDIRM/Zg_strong222.root Zg_strong222*root
rm Wg_strong222*root
rm Zg_strong222*root
hadd $OUTDIRM/Zg_strongFxFx.root Zg_strongFxFx*root
rm Zg_strongFxFx*root

hadd $OUTDIRM/Wg_strong.root Wg_strong*root
hadd $OUTDIRM/Zg_strong.root Zg_strong*root
hadd $OUTDIRM/ttg.root ttg*root
##hadd $OUTDIRM/SinglePhotonBCL.root SinglePhotonBCL*root
##rm SinglePhotonBCL*root
hadd $OUTDIRM/SinglePhoton.root SinglePhoton*root
hadd $OUTDIRM/VqqGam.root VqqGam*root
hadd $OUTDIRM/ggFHgamdark125.root ggFHgamdark125*root
hadd $OUTDIRM/VBFHgamdark125.root VBFHgamdark125*root

# for the gamma ones:
echo "mv $OUTDIRM/ttbar.root ttbar.root"
echo "hadd $OUTDIRM/ttbar.root ttbar.root $OUTDIRM/ttg.root "
echo "mv $OUTDIRM/Zg_EWK.root Zg_EWK.root"
echo "hadd $OUTDIRM/Zg_EWK.root Zg_EWK.root $OUTDIRM/Z_EWK.root "
echo "mv $OUTDIRM/Wg_EWK.root Wg_EWK.root"
echo "hadd $OUTDIRM/Wg_EWK.root Wg_EWK.root $OUTDIRM/W_EWK.root "
echo "mv $OUTDIRM/Zg_strong.root Zg_strong.root"
echo "hadd $OUTDIRM/Zg_strong.root Zg_strong.root $OUTDIRM/Z_strong.root  $OUTDIRM/Z_strongExt.root"
echo "mv $OUTDIRM/Wg_strong.root Wg_strong.root"
echo "hadd $OUTDIRM/Wg_strong.root Wg_strong.root $OUTDIRM/W_strong.root $OUTDIRM/W_strongExt.root"
echo "mv $OUTDIRM/VBFHgam125.root VBFHgam125.root"
echo "hadd $OUTDIRM/VBFHgam125.root VBFHgam125.root $OUTDIRM/VBFH125.root"
for i in "Z_strongExt" "W_strongExt" "Z_strong" "W_strong" "ttg" "VBFH125" "Z_EWK" "W_EWK" ; do
    echo "rm $OUTDIRM/${i}.root ${i}.root"
done


echo "hadd $OUTDIRM/VBFHgamdark1000.root VBFHgamdark1000*root"
echo "rm VBFHgamdark1000*root"
echo "hadd $OUTDIRM/VBFHgamdark2000.root VBFHgamdark2000*root"
echo "rm VBFHgamdark2000*root"
echo "hadd $OUTDIRM/VBFHgamdark3000.root VBFHgamdark3000*root"
echo "rm VBFHgamdark3000*root"
echo "hadd $OUTDIRM/ggFHgamdark125.root ggFHgamdark125*root"
echo "hadd $OUTDIRM/VBFHgamdark125Old.root VBFHgamdark125Old*root"
echo "rm VBFHgamdark125Old*root"
echo "hadd $OUTDIRM/VBFHgamdark125.root VBFHgamdark125*root"
echo "hadd $OUTDIRM/VBFHgamdark500.root VBFHgamdark500*root"
echo "hadd $OUTDIRM/VBFHgamdark400.root VBFHgamdark400*root"
echo "hadd $OUTDIRM/VBFHgamdark300.root VBFHgamdark300*root"
echo "hadd $OUTDIRM/VBFHgamdark250.root VBFHgamdark250*root"
echo "hadd $OUTDIRM/VBFHgamdark200.root VBFHgamdark200*root"
echo "hadd $OUTDIRM/VBFHgamdark150.root VBFHgamdark150*root"
echo "hadd $OUTDIRM/VBFHgamdark100.root VBFHgamdark100*root"
echo "hadd $OUTDIRM/VBFHgamdark80.root VBFHgamdark80*root"
echo "hadd $OUTDIRM/VBFHgamdark60.root VBFHgamdark60*root"

