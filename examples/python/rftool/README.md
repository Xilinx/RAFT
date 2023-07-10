<h1> Usage Description of rftool </h1>

<p>Rftool class inherits RFDC, RFCLK and AXI_MEMMAP client classes. Also, it have functionalities required for the configuration and getting data from STIM and CAP modules of ZCU208 and ZCU216 board reference xsa (The xsa in the released bsp - https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools/2022-2.html). The file rftool.py is a pythonic implementation of 'Rftool' application mentioned in ug1433 (https://www.xilinx.com/support/documents/boards_and_kits/zcu216/ug1433-zcu216-rfsoc-eval-tool.pdf), Chapter 4, Software Design and Build secton. The data transfer support is  implemented only for BRAM mode. Data transfer support over DDR is not added at the moment.</p>

<p>mixer.py is a sample application written over rftool.py. For more details please refer pg269 document (https://docs.xilinx.com/v/u/2.4-English/pg269-rf-data-converter). mixer.ipynb is the jupyter notebook equivalent of mixer.py. </p>

<h2>Petalinux Build</h2>

<p>For steps to prepare the petalinux build required for running mixer.py, follow the same steps for building petalinux with raft. In the raft recipe, (Step 6: Create raft library recipe) change xpyro-prj1 to xpyro-prj2</p>
<p>For preparing the build for running the jupyter notebook example (mixer.ipynb), follow the steps mentioned in RAFT/docs/build_petalinux_jupyternb_raft.txt</p>

<h2>Hardware setup</h2>

<p>Setup as mentioned in https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/246153525/RF+DC+Evaluation+Tool+for+ZCU216+board+-+Quick+start. Connect CLK0104 and XM655/616B as shown in the diagram. Instead of RF Data Converter Evaluation User Interface, this application can be used.</p>

<h2>Usage</h2>
<p>The Rftool class runs at the host (Windows or Linux) PC</p>
<p>At the board project inside xserver/init/xpyro-prj2 folder is used</p>
<h3>At Board</h3>
<p>In the serial console of the board give the following commands</p>
<ul>cd /usr/share/raft/xserver/init/xpyro-prj2</ul>
<ul>python3 <i>__init__.py</i> </ul>
<p>Note: No need to run this, if it is already present in the starup-script.</p>
<h3>At Host</h3>
<p>Clone the github repository</p>
<ul>git clone https://github.com/Xilinx/RAFT</ul>
<p>Change directory to the rftool folder</p>
<ul>cd RAFT/xserver/examples/python/rftool</ul>
<ul>Run the test application.</ul>
<ul>python3 <i>mixer.py</i></ul>
<p>If jupyter notebook is enabled as per RAFT/docs/build_petalinux_jupyternb_raft.txt, enter the link to jupyter notebook in the browser.</p>
<ul>Eg: http://169.254.10.2:8888/</ul>

Copyright (C) 2022 - 2023 Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: BSD-3-Clause

