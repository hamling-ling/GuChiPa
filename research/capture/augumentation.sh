rm -rf flp rot scl trs crp cnt gam

# x2
python flip.py raw flp
# x3
python rot.py flp rot
# x3
python scale.py rot scl
# x9
python trans.py scl trs
# x1
python crop.py trs crp
# x3
python contrast.py crp cnt
# x3
python gamma.py cnt gam
# x2
#python gaussnoise.py
# x3
#python saltnoise.py


