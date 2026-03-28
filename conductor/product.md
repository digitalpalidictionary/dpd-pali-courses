# Product Definition

## Initial Concept
So is the goal is to hold the source material for the pali course and build a website Html website from that source which located in the docs folder and also maintain the pali course so if there are any errors if there is any mistake or aditions they would be adjusted in the MD files and then by the workflow automatically by me pushing it as they would build the website so basically this is a repo where we hold the course material with the exercise key for exercise, etc.

## Vision
To serve as the definitive, version-controlled source for Digital Pāli Dictionary (DPD) course materials, enabling collaborative maintenance and automated publishing of a high-quality educational website.

## Target Audience
- Buddhist practitioners and monastics seeking to study original Pāḷi texts.
- Educators and students participating in the DPD Pāḷi courses.

## Core Features
- **Markdown Source of Truth:** Centralized storage of course lessons, exercises, and answer keys in human-readable Markdown.
- **Automated Web Publishing:** A CI/CD workflow using MkDocs and Material for MkDocs that transforms Markdown source into a functional HTML website upon every update.
- **Automated PDF Export:** A CI/CD workflow that transforms Markdown sources into styled PDF documents upon every update, utilizing the same CSS as the website.
- **Collaborative Maintenance:** An environment where corrections, improvements, and additions to the course material can be tracked and managed via Git.
- **Resource Bundling:** Tools (like Python scripts) to package and distribute materials for offline study.
