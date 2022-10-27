<h1> Usage Description of rftool </h1>

<p>Rftool class inherits RFDC, RFCLK and AXI_MEMMAP client classes. Also, it have functionalities required for the configuration and getting data from STIM and CAP modules of ZCU208 and ZCU216 board reference xsa. The file rftool.py is a pythonic implementation of 'Rftool' application mentioned in ug1433 (https://www.xilinx.com/support/documents/boards_and_kits/zcu216/ug1433-zcu216-rfsoc-eval-tool.pdf), Chapter 4, Software Design and Build secton. The data transfer support is only implemented only for BRAM. Data transfer support over DDR is not added  at the moment.</p>

<p>mixer.py is a sample application written over rftool.py. For more details please refer pg269 document (https://docs.xilinx.com/v/u/2.4-English/pg269-rf-data-converter). mixer.ipynb is the jupyter notebook equivalent of mixer.py. </p>

<h2>Petalinux Build</h2>

<p>For steps to prepare the build petalinux required for running mixer.py follow the same steps for building petalinux with raft (RAFT/docs/build_petalinux_with_raft.txt) and add required contents of this rftool folder (rftool.py and mixer.py) as well in the raft recipe list (Step 6: Create raft library recipe)</p>
<p>For preparing the build for running the jupyter notebook example (mixer.ipynb), please follow the steps mentioned in RAFT/docs/build_petalinux_jupyternb_raft.txt</p>

<h2>Usage</h2>
<p>The Rftool class runs at the host (Windows or Linux) PC</p>
<p>At the board project inside xserver/init/xpyro-prj2 folder is used</p>
<h3>At Board</h3>
<p>In the serial console of the board give the following commands</p>
<ul>cd /usr/share/raft/xserver/init/xpyro-prj2</ul>
<ul>python3 <i>__init__.py</i> </ul>
<h3>At Host</h3>
<ul>cd /usr/share/raft/xserver/examples/python/rftool</ul>
<ul>Run the desired test application. For example,</ul>
<ul>python3 <i>mixer.py</i></ul>
