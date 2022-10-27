README for "Example1" Python Scripts
====================================

The "example1" python scripts provide getting started examples for using the RAFT framework with the 
UG1530 RFSoC DFE Targeted Reference Design. Refer to UG1530 for more details on building hardware and software parts of the reference design and system bring-up.

These scripts provide a starting point for scripting and are designed to work with the 2-antenna reference design "zcu670_rfsoc_dfe2x1111p1111bw491_cmcd_emcp_refd". 
Scripts for other designs may vary but will follow same basic flow. 

Vivado ILAs (Integrated Logic Analysers) are available in many designs to monitor nodes within the design. Refer to IP Integrator Block Diagram for interconnection of blocks.

A list of example scripts supplied are given below, in order of data flow down the downlink and then up the uplink chains. CFR and DPD IP have their own control applications.

| Script                 |    Description                    |
|:-----------------------|:----------------------------------|
| common_example1.py     | Common Code used by other scripts |
| stimcap_example1.py    | BRAM Stimulus Example             |
| ccseq_example1.py      | CC Sequence Example               |
| ccf_example1.py        | DFE Channel Filter Example        |
| mix_example1.py        | DFE DUC/DDC Mixer Example         |
| vmux_example1.py       | Setup Uplink Loopback             |
| equ_example1.py        | DFE Equalizer Example             |
| rfdc_example1.py       | RF Data Converter Example         |