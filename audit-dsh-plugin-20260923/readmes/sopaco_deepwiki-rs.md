<p align="center">
  <img height="160" src="./assets/banner_litho.webp">
</p>

<h3 align="center">Litho (deepwiki-rs)</h3>

<p align="center">
    <a href="./README.md">English</a>
    |
    <a href="./README_zh.md">中文</a>
</p>
<p align="center">💪🏻 High-performance <strong>AI-driven</strong> intelligent document generator (DeepWiki-like) built with <strong>Rust</strong></p>
<p align="center">📚 Automatically generates high quality <strong>Repo-Wiki</strong> for any codebase</p>

<p align="center">
  <a href="https://crates.io/crates/deepwiki-rs"><img src="https://img.shields.io/crates/v/deepwiki-rs?color=44a1c9" /></a>
  <a href="https://crates.io/crates/deepwiki-rs"><img src="https://img.shields.io/crates/d/deepwiki-rs.svg" /></a>
  <a href="https://github.com/sopaco/deepwiki-rs/tree/main/docs/en"><img alt="Litho Docs" src="https://img.shields.io/badge/Litho-Docs-green?logo=Gitbook&color=%23008a60"/></a>
  <a href="https://github.com/sopaco/deepwiki-rs/tree/main/docs/zh"><img alt="Litho Docs" src="https://img.shields.io/badge/Litho-中文-green?logo=Gitbook&color=%23008a60"/></a>
  <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/sopaco/deepwiki-rs/rust.yml">
</p>

<div align="center">
  <a href="https://trendshift.io/repositories/67975?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-67975" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/67975/daily?language=Rust" alt="sopaco%2Fdeepwiki-rs | Trendshift" width="250" height="55"/></a>
  <a href="https://trendshift.io/repositories/67975?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-67975" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/67975" alt="sopaco%2Fdeepwiki-rs | Trendshift" width="250" height="55"/></a>
</div>

<hr />

<div align="center">

**🚀 Litho has evolved into [Terrain](https://github.com/sopaco/terrain)** — give your AI agents a living map of your codebase.

<p align="center">
  <a href="https://github.com/sopaco/terrain"><img width="360" alt="Terrain — agent environment managements" src="./assets/snapshot_terrain_agent_environmen_ managements.webp"></a>
  <a href="https://github.com/sopaco/terrain"><img width="360" alt="Terrain — engineering knowledge assets" src="./assets/snapshot_terrain_engineering_knowledge_assets.webp"></a>
</p>

<sub>On top of Litho: knowledge base stays in sync with code · broader language & framework support · mainstream agents (Claude Code, Codex, DeepSeek Harness…) read it via ACP · Litho Book built in.</sub>

**[Check out Terrain →](https://github.com/sopaco/terrain)** &nbsp;·&nbsp; *Litho stays the fast, focused C4 doc generator.*

</div>

# 👋 What's Litho

**Litho** is an AI-powered documentation generation engine that automatically analyzes your source code and generates comprehensive, professional architecture documentation in the C4 model format. No more manual documentation that falls behind code changes - Litho keeps your documentation perfectly in sync with your codebase.

Litho transforms raw code into beautifully structured documentation with context diagrams, container diagrams, component diagrams, and code-level documentation - all automatically generated from your source code.

Whether you're a developer, architect, or technical lead, Litho eliminates the burden of maintaining documentation and ensures your team always has accurate, up-to-date architectural information.

<p align="center">
  <strong>Transform your codebase into professional architecture documentation in minutes</strong>
</p>

<div style="text-align: center; margin: 30px 0;">
  <table style="width: 100%; border-collapse: collapse; margin: 0 auto;">
    <tr>
      <th style="width: 50%; padding: 15px; background-color: #f8f9fa; border: 1px solid #e9ecef; text-align: center; font-weight: bold; color: #495057;">Before Litho</th>
      <th style="width: 50%; padding: 15px; background-color: #f8f9fa; border: 1px solid #e9ecef; text-align: center; font-weight: bold; color: #495057;">After Litho</th>
    </tr>
    <tr>
      <td style="padding: 15px; border: 1px solid #e9ecef; vertical-align: top;">
        <p style="font-size: 14px; color: #6c757d; margin-bottom: 10px;"><strong>Manual Documentation</strong></p>
        <ul style="font-size: 13px; color: #6c757d; line-height: 1.6;">
          <li>Outdated, incomplete, or missing documentation</li>
          <li>Manual updates that fall behind code changes</li>
          <li>Inconsistent formatting and structure</li>
          <li>Time-consuming to maintain</li>
          <li>Hard to navigate and understand</li>
          <li>Usually just a few markdown files</li>
        </ul>
      </td>
      <td style="padding: 15px; border: 1px solid #e9ecef; vertical-align: top;">
        <p style="font-size: 14px; color: #6c757d; margin-bottom: 10px;"><strong>AI-Generated Documentation</strong></p>
        <ul style="font-size: 13px; color: #6c757d; line-height: 1.6;">
          <li>Automatically generated from codebase</li>
          <li>Always up-to-date with code changes</li>
          <li>Professional C4 model structure</li>
          <li>Consistent formatting and styling</li>
          <li>Easy to navigate and understand</li>
          <li>Complete with diagrams, context, and relationships</li>
        </ul>
      </td>
    </tr>
  </table>
</div>

<p align="center">
  <strong>🚀 Litho automatically transforms your messy codebase into beautiful, professional documentation</strong>
</p>

<hr />

# 😺 Why use Litho

- **Automatically keep documentation in sync** with codebase changes - no more outdated docs
- **Save hundreds of hours** on manual documentation creation and maintenance
- **Improve onboarding** for new team members with comprehensive, up-to-date documentation
- **Enhance code reviews** by providing clear architectural context
- **Meet compliance requirements** with auditable, automated documentation
- **Support for multiple programming languages** (Rust, Python, Java, Go, C#, JavaScript, etc.)
- **Generate professional C4 model diagrams** with context, containers, components, and code
- **Integrate with CI/CD pipelines** to automatically generate documentation on every commit

🌟 **For:**
- Development teams of all sizes
- Open source projects
- Enterprise software developers
- Anyone who hates maintaining outdated docs!

❤️ Like **Litho**? Star it 🌟 or [Sponsor Me](https://github.com/sponsors/sopaco)! ❤️

**Thanks to the kind people**

[![Stargazers repo roster for @sopaco/deepwiki-rs](https://reporoster.com/stars/sopaco/deepwiki-rs)](https://github.com/sopaco/deepwiki-rs/stargazers)

# 🌠 Features & Capabilities

### Core Capabilities
- AI-driven architecture documentation generation from codebase analysis
- Automatic C4 model diagram creation (Context, Container, Component, Code)
- Intelligent extraction of code comments, structures, and relationships
- Multi-language support for various programming languages
- Customizable template system for documentation output

### Advanced Features
- **External Knowledge Integration** - Mount external documentation (PDF, Markdown, SQL, etc.) as knowledge sources for enhanced analysis
- **Database Documentation** - Auto-generate database schema documentation with ERD diagrams for SQL projects
- Git history analysis for tracking architectural evolution
- Cross-referencing between code elements and documentation
- Interactive documentation with embedded diagrams and examples
- Integration with CI/CD pipelines for automated documentation generation

## 💡 Problem Solved
Litho solves the common problem of outdated and incomplete technical documentation by automatically generating up-to-date architecture documentation from your source code. No more manual documentation that falls behind code changes - Litho keeps your documentation in sync with your codebase.

# 🌐 Litho Eco 