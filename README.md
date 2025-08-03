# Hardcoded Pswd Analysis Tool

**Author:** Jacob Lord  
**Year:** 2025

## Overview

The **Hardcoded Pswd Analysis Tool** is a cybersecurity-focused static code analysis utility designed to detect and flag hardcoded passwords within source code. This tool aims to reduce the risk of backdoor attacks by identifying credentials that may have been inadvertently left in code before deployment.

## Purpose

Hardcoded passwords are a common yet critical security vulnerability that can lead to unauthorized access and compromise of systems. This tool helps software teams proactively:

- Audit source code for embedded credentials.
- Identify risky patterns before production release.
- Enforce secure coding practices in development pipelines.

## Features

- Scans multiple file types for password-like patterns.
- Customizable detection rules.
- Generates easy-to-read reports of findings.
- Lightweight and scriptable for CI/CD integration.

## Use Cases

- Pre-commit or pre-merge security checks.
- Continuous Integration (CI) pipelines.
- Manual audits during security reviews.
- Teaching secure coding practices.

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/hardcoded-pswd-analysis-tool.git
cd hardcoded-pswd-analysis-tool
