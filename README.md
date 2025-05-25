# Notice
This repository is created for the paper "AutoP2C: An LLM-Based Agent Framework for Code Repository Generation from Multimodal Content in Academic Papers." In this paper, we focus on how to automatically generate a code repository for an academic paper with multimodal content and call it the ``Paper-to-Code'' (P2C) task,as shown in Figure 1.
![illus](intro.jpg)

Specifically, given a research paper containing heterogeneous, multimodal content, P2C aims to generate a complete executable code repository that accurately implements the described methods and reproduces the reported results.

To fill this research-to-implementation gap, we propose AutoP2C, a multi-agent framework specifically designed to generate complete code repositories from the multimodal content of research papers, as shown in Figure 2.
![process](process(5).png)

AutoP2C comprises four stages. In the first stage, it extracts universal code structures from established repositories to construct architectural blueprints. The next stage involves multimodal content parsing, which integrates information from text, diagrams, and tables into a unified representation. In the third stage, divide-and-conquer task planning decomposes complex implementations into hierarchical subtasks with clearly defined interfaces. 
Finally, execution feedback-driven debugging localizes errors and aligns the code with the multimodal specifications of the paper through iterative testing. Unlike previous approaches that treat code generation as a unimodal text-to-text translation problem, AutoP2C takes advantage of multimodal understanding to capture the full spectrum of information presented in academic papers. 
We have now released an initial version of the code. You can have a try by following the steps.  

You can first translate the paper using MinerU and put the transformed paper content under markdown_files/paper.md. Then, execute the run.sh.
