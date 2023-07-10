<h1> Usage Description of python examples </h1>


<p>Python usage scripts run in three modes.</p>
<p>xclient - Runs at host (Windows or Linux) PC or at board communicating with xclient</p>
<p>xcffi - Runs at board directly communicating with xcffi without pyro</p>
<p>xpyro - Runs at host (Windows or Linux) PC or at board communicating with pyro server</p>
<p>To run the xclient at host, Python 3.7 or higher with Pyro4 package is required.<p>
<p>Package installation command for Pyro4 is given below<p>
<i>pip install Pyro4<i>

<h2>Mode - xclient</h2>

<p>Runs at host (Windows or Linux) PC or at board communicating with xclient</p>
<h3>To run at host (Windows or Linux) PC</h3>
<p>Run the python script,</p>
<ul>python3 <i>script_name</i> xclient host ip_address port</ul>
<h3>To run at board</h3>
<p>In the serial console of the board give the following commands</p>
<ul>cd /usr/share/examples/python</ul>
<ul>sudo python3 <i>script_name</i> xclient board ip_address port</ul>

<h2>Mode - xcffi</h2>

<p>Runs at board directly communicating with xcffi</p>

<p>In the serial console of the board give the following commands</p>
<ul>cd /usr/share/examples/python</ul>
<ul>sudo python3 <i>script_name</i> xcffi</ul>

<h2>Mode - xpyro</h2>

<p>Runs at host (Windows or Linux) PC or at board communicating with pyro server</p>
<h3>To run at host (Windows or Linux) PC</h3>
<p>Run the python script,</p>
<ul>python3 <i>script_name</i> xpyro host ip_address port</ul>
<h3>To run at board</h3>
<p>In the serial console of the board give the following commands</p>
<ul>cd /usr/share/examples/python</ul>
<ul>python3 <i>script_name</i> xpyro board ip_address port</ul>

Copyright (C) 2022 - 2023 Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: BSD-3-Clause