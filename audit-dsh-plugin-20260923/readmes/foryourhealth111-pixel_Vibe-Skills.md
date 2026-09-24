<div align="right">
  <strong>English</strong> | <a href="./README.zh.md">中文</a>
</div>

<div align="center">

<img src="./logo.png" width="124" alt="VibeSkills logo">

<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/readme-wordmark-dark.svg">
    <img src="./docs/assets/readme-wordmark-light.svg" width="500" alt="VibeSkills">
  </picture>
</h1>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/readme-tagline-en-dark.svg">
  <img src="./docs/assets/readme-tagline-en-light.svg" width="560" alt="VibeSkills is a general-purpose Skill that automatically routes local Skills and intelligently orchestrates harness workflows.">
</picture>

<br>

<a href="https://github.com/foryourhealth111-pixel/Vibe-Skills/releases/latest">
  <strong>Latest release · v4.1.0</strong>
</a>

<br>

<a href="./docs/install/README.en.md">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/install-cta-en-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./docs/assets/install-cta-en-light.svg">
    <img src="./docs/assets/install-cta-en-light.svg" width="210" height="38" alt="Install VibeSkills">
  </picture>
</a>

<br>

<a href="./docs/quick-start.en.md">Quick start</a> ·


</div>

<a id="skillsbench-performance"></a>
<h2 align="center">Measured on SkillsBench</h2>

<p align="center">
  <strong>Mean verifier reward: +21.12 pp</strong><br>
  <strong>Total tokens: -29.6%</strong> · <strong>Tool calls: -33.1%</strong>
</p>

**SkillsBench** is a benchmark designed to evaluate whether AI agents can effectively use Skills to complete professional tasks across diverse domains. Its purpose is to measure how much a model’s ability to solve complex real-world tasks improves when it is equipped with specialized Skills.

To evaluate performance in production-like environments where a large number of Skills are installed simultaneously, we adapted SkillsBench into a more realistic **large-scale multi-Skill setting**. In the original SkillsBench setup, each task is provided only with the specialized Skill associated with that task. In our modified setting, every task is evaluated in a global environment containing all **195 specialized Skills**, while all other experimental conditions remain unchanged. This setting is intended to assess whether an agent can autonomously discover, select, and orchestrate the relevant Skills from a large installed Skill pool, and organize them into an effective workflow for completing complex tasks.

**vibeskills v4.1.0** was benchmarked on **SkillsBench** (https://www.skillsbench.ai/) using **DeepSeekV4Flash-VE** and **OpenHands** as the baseline evaluation setup. Compared with the baseline without vibeskills, vibeskills increased the **average task score by 21.12%**, while reducing **token consumption by 29.6%** and **tool calls by 33.1%**.


<p align="center">
  <a href="https://github.com/foryourhealth111-pixel/vibeskills-benchmark/tree/main/studies/full-skills-comparison">
    <img src="./docs/assets/skillsbench-task-outcomes.png" width="900" alt="SkillsBench paired task outcomes: Lean Vibe increased mean reward from 50.3% to 71.4%, increased the full-score rate from 47.6% to 69.5%, scored higher on 23 tasks, tied on 55, and scored lower on 4">
  </a>
</p>

<p align="center"><sub>Task quality: 39 to 57 full-score tasks; Lean Vibe scored higher on 23 tasks, Native on 4, with 55 ties.</sub></p>

<p align="center">
  <a href="https://github.com/foryourhealth111-pixel/vibeskills-benchmark/tree/main/studies/full-skills-comparison">
    <img src="./docs/assets/skillsbench-resource-use.png" width="900" alt="SkillsBench resource comparison: total token use fell from 491.1 million for Native to 345.8 million for Lean Vibe, while tool calls fell by 33.1%">
  </a>
</p>

<p align="center"><sub>Resource use: 491.122M to 345.756M total tokens, with tool calls reduced from 9,954 to 6,664.</sub></p>

Analysis of the logs from the original benchmark shows that ***VibeSkills achieves better task performance not by invoking more Skills***.

Instead, it first clarifies the task objective and delivery requirements, then decomposes a complex task into several verifiable subtasks. It subsequently selects only a small number of truly relevant capabilities from a large pool of candidate Skills and executes them in an order determined by their dependencies. This helps reduce misunderstandings of the task, omitted steps, and incorrect Skill selection, thereby improving overall task performance.

***In terms of token cost and tool usage***, this workflow also eliminates a substantial amount of ineffective trial and error. Native agents are more likely to repeatedly invoke tools in unproductive directions, reread the same context, and redo previous work. In contrast, VibeSkills converges more quickly on the critical steps through clearer planning and pre-delivery checks. As a result, it not only improves task quality, but also significantly reduces tool-call loops and the token overhead caused by repeated context processing.


<p align="center">
  <a href="https://github.com/foryourhealth111-pixel/vibeskills-benchmark/blob/main/studies/full-skills-comparison/README.md">Study, public data, and reproduction</a> ·
</p>


<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./docs/assets/readme-preface-v2-en-mobile-dark.svg">
    <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset="./docs/assets/readme-preface-v2-en-mobile-light.svg">
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/readme-preface-v2-en-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./docs/assets/readme-preface-v2-en-light.svg">
    <img src="./docs/assets/readme-preface-v2-en-light.svg" width="900" alt="Skills are excellent local assets of reusable experience. After downloading and installing many Skills, it is easy to sometimes forget which Skills have already been installed and not know which Skills to invoke. Further, when a complex task involves the combined organization and invocation of multiple Skills from different domains, planning becomes complicated for people: they must explain to the AI in detail which Skills each module should use, while the AI may forget these designs during execution. Many current harness frameworks do not actively plan how to make good use of local Skill resources, and may even fall into an either-or scheduling conflict between the harness framework and domain Skill resources. The core of this project is to follow harness frameworks similar to Superpower and GSD. Based on modular decomposition by the planning state machine, it uses different Skills to assist different modules, fully schedules existing local resources, reduces users' planning and cognitive burden, and gives users an end-to-end delivery experience. It is committed to becoming a handy steward for the Skill resources around you. When a complex task appears, it can help users slowly sort out which modules are needed and which good experiences can be reused, then deliver an excellent result.">
  </picture>
</p>

<a id="vibeskills-ml-practice-case"></a>
<h2 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/readme-chapter-01-en-dark.svg">
    <img src="./docs/assets/readme-chapter-01-en-light.svg" width="720" alt="VibeSkills Practice Case: Completing a Machine-Learning Experiment">
  </picture>
</h2>

> **Task**
>
> *Use public data to complete a reproducible classification experiment and deliver a data audit, statistical review, 4 result figures, a scientific report, and a 7-slide group-meeting deck.*

The diagram shows what happened after the requirement and plan were approved:
how the task was executed, what it produced, and how the result was checked.

The task used the `L` workflow and proceeded in order. During public