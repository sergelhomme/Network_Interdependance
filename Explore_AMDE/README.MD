Guide d’installation de l’outil permettant d’explorer des AMDE

Cet outil vise à automatiser la production de scénarios potentiellement obtenus par une AMDE. Il propose des synthèses quantitatives pouvant permettre de questionner l’AMDE construite et de la modifier en cas de problèmes clairement identifiés. Cet outil n’est aucunement conçu pour concevoir les AMDE. Il repose sur un tableau de type csv (séparateur de type « , ») comportant six colonnes correspondant : au numéro de la fonction ; au nom du système ; au nom du composant ; à la description de la défaillance ; aux causes de défaillances ; aux effets de ces défaillances. Ce tableau doit être nommé « amde.csv » et placé dans le dossier « Explore_AMDE ». Un exemple de ce fichier est déjà présent dans le dossier « Explore_AMDE », il ne reste plus qu’à le remplacer par le vôtre. Cet outil s’appuie sur une production rigoureuse de l’AMDE, notamment en ce qui concerne l’identification des causes et des effets. Chaque effet, comme chaque cause, doit être séparé par un « ; ».

Cet outil fonctionne à partir de python. Pour cela, il vous faudra simplement disposer d’une version de python comportant les bibliothèques Scipy, Matplotlib et Networkx. Les deux premières sont très courantes (il se peut que vous les ayez déjà installées), l’installation de NetworkX est alors très simple (rapportez-vous au troisième item). Si vous partez de zéro, suivez les items ci-dessous un par un. Le dossier « Explore_AMDE » peut être placé n’importe où dans vos documents, l’ouverture de l’interface se fera par un simple double-clic sur le fichier « run_amde.py ».

1) Commencez par installer Python et deux bibliothèques courantes. Pour cela, choisissez l’option la plus simple en utilisant les versions stables et bénéficiant d’un installeur (les fichiers .msi ou .exe pour windows)
Installation de Python 3.4.4
https://www.python.org/downloads/release/python-344/
Pour windows : https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi
Laissez tous les paramètres par défaut.
Installation Numpy
https://sourceforge.net/projects/numpy/files/NumPy/1.10.2/
Pour windows : https://sourceforge.net/projects/numpy/files/NumPy/1.10.2/numpy-1.10.2-win32-superpack-python3.4.exe/download
Laissez tous les paramètres par défaut.
Installation Scipy
https://sourceforge.net/projects/scipy/files/scipy/0.16.1/
Pour windows : https://sourceforge.net/projects/scipy/files/scipy/0.16.1/scipy-0.16.1-win32-superpack-python3.4.exe/download
Laissez tous les paramètres par défaut.

-------------------------
2) Continuez avec l’installation de MatplotLib
https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/windows/matplotlib-1.4.3.win32-py3.4.exe
Matplotlib nécessite ensuite l’installation de :
https://pypi.python.org/pypi/six
Prenez le tar.gz décompressez le dossier. Copiez le fichier six.py dans « C:\Python34\Lib\site-packages ».
https://pypi.python.org/pypi/python-dateutil/2.4.1
Prenez le zip décompressez le dossier. Copiez le dossier dateutil dans « C:\Python34\Lib\site-packages ».
https://pypi.python.org/pypi/pyparsing/2.0.3
Prenez le zip décompressez le dossier. Copiez le fichier pyparsing.py dans « C:\Python34\Lib\site-packages ».

-------------------------
3) Enfin, vous pouvez procéder à l’installation de la bibliothèque NetworkX qui permet d’effectuer de nombreux calculs sur les graphes.
https://pypi.python.org/packages/3b/d4/1b6ca16678d13ffd426bcd199231f3d5effaa6d234747fb88899e649dec3/networkx-1.11.zip
Dézippez le dossier zippé. Ensuite, dans le dossier networkx.1.11 dézippé, copiez le dossier networkx dans « C:\Python34\Lib\site-packages »
https://pypi.python.org/pypi/decorator
Prenez le tar.gz décompressez le dossier. Copiez le fichier decorator.py dans « C:\Python34\Lib\site-packages ».
