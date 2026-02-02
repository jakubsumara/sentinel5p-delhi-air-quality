# GitHub Upload Guide

## ✅ Repository Prepared

Your project is now ready to be uploaded to GitHub! Git has been initialized and all files have been staged.

## 📋 Step-by-Step Instructions

### Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository Settings:**
   - **Repository name:** `sentinel5p-delhi-air-quality` (or your preferred name)
   - **Description:** `Sentinel-5P Air Pollution Dynamics over Delhi NCR - 24-month analysis`
   - **Visibility:** Choose Public or Private
   - **⚠️ IMPORTANT:** Do NOT check any of these:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   - Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/sentinel5p-delhi-air-quality.git
```

### Step 3: Commit and Push

```bash
# Make initial commit
git commit -m "Initial commit: Complete Sentinel-5P analysis project

- 24-month analysis of NO2, SO2, CO, HCHO over Delhi NCR
- Local vs. advected pollution classification
- Source attribution maps with back-trajectories
- Complete workflow with reproducible scripts
- 5-minute presentation included"

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Verify Upload

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality`
2. Verify that all files are present
3. Check that README.md displays correctly

## 🚀 Quick Commands (Copy-Paste Ready)

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# 1. Add remote
git remote add origin https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality.git

# 2. Commit
git commit -m "Initial commit: Complete Sentinel-5P analysis project"

# 3. Push
git branch -M main
git push -u origin main
```

## 📝 What's Included

The repository includes:

- ✅ All analysis scripts (`scripts/`)
- ✅ Main workflow script (`run_analysis.py`)
- ✅ Configuration file (`config.py`)
- ✅ Complete documentation (README, WORKFLOW, etc.)
- ✅ Jupyter notebook (`notebooks/`)
- ✅ Output visualizations (`outputs/maps/`, `outputs/time_series/`)
- ✅ Presentation slides (`outputs/presentation/`)
- ✅ Interpretive note (`outputs/reports/`)
- ✅ Setup scripts and guides

**Excluded (via .gitignore):**
- Large data files (`data/era5/`, `data/processed/*.nc`, `*.tif`)
- Credentials (`.cdsapirc`, `earthengine-credentials.json`)
- Python cache files (`__pycache__/`)
- Virtual environments (`venv/`)

## 🔐 Important Notes

### Credentials
- **Never commit credentials!** The `.gitignore` excludes:
  - `.cdsapirc` (ERA5 API key)
  - `earthengine-credentials.json` (GEE credentials)
  - Any `.json` files that might contain keys

### Large Files
- Data files are excluded (too large for GitHub)
- Users will need to download data themselves using the provided scripts
- See `WORKFLOW.md` for data download instructions

### First Push
- If you get authentication errors, you may need to:
  - Use a Personal Access Token instead of password
  - Set up SSH keys
  - Use GitHub Desktop or GitHub CLI

## 🎯 After Upload

1. **Update README.md:**
   - Replace `YOUR_USERNAME` with your actual GitHub username
   - Update author information
   - Add your contact email

2. **Add Topics/Tags:**
   - Go to repository settings
   - Add topics: `sentinel-5p`, `air-quality`, `delhi`, `satellite-data`, `python`, `earth-observation`

3. **Create Releases (Optional):**
   - Tag your first commit: `git tag -a v1.0 -m "Initial release"`
   - Push tags: `git push origin v1.0`

4. **Enable GitHub Pages (Optional):**
   - Go to Settings > Pages
   - Enable GitHub Pages to showcase your project

## 🆘 Troubleshooting

### Authentication Issues
```bash
# Use Personal Access Token
# Or set up SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
# Then add to GitHub: Settings > SSH and GPG keys
```

### Large File Issues
```bash
# If you accidentally added large files:
git rm --cached data/era5/*.nc
git commit -m "Remove large data files"
```

### Remote Already Exists
```bash
# Remove existing remote
git remote remove origin
# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality.git
```

## ✅ Verification Checklist

Before pushing, verify:
- [ ] All sensitive files are in `.gitignore`
- [ ] README.md is updated with your information
- [ ] No large data files are staged
- [ ] All scripts are tested and working
- [ ] Documentation is complete

## 📞 Need Help?

- GitHub Docs: https://docs.github.com/en/get-started
- Git Handbook: https://guides.github.com/introduction/git-handbook/
- GitHub Desktop: https://desktop.github.com/ (GUI alternative)

---

**Ready to upload!** Follow the steps above to get your project on GitHub. 🚀
