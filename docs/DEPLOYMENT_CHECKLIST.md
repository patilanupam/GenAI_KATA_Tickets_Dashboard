# 🚀 Deployment Checklist for ClarifyMeet AI (Streamlit)

Use this checklist to ensure smooth deployment of your Streamlit app.

## 📋 Pre-Deployment Checklist

### Local Testing

- [ ] **Python version verified**
  ```bash
  python --version  # Should be 3.11+
  ```

- [ ] **Ollama installed and running**
  ```bash
  curl http://localhost:11434/api/tags
  ```

- [ ] **TinyLlama model downloaded**
  ```bash
  ollama list  # Should show tinyllama
  ```

- [ ] **Dependencies installed**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **App launches successfully**
  ```bash
  streamlit run streamlit_app.py
  ```

- [ ] **Test with sample transcript**
  - Upload `clarifymeet_meetings/easy_meeting.txt`
  - Verify processing completes
  - Check all tabs display correctly

- [ ] **Download functionality works**
  - Click "Download JSON Results"
  - Verify file downloads correctly

### Code Quality

- [ ] **No sensitive data in code**
  - Check `.streamlit/secrets.toml` not committed
  - Verify `.env` files not in git
  - Review `.gitignore` is complete

- [ ] **Documentation is complete**
  - README.md updated
  - QUICKSTART_STREAMLIT.md reviewed
  - STREAMLIT_DEPLOYMENT.md checked

- [ ] **Error handling tested**
  - Try uploading non-.txt file
  - Test with empty file
  - Test with very large file (>10MB)

## 🌐 Streamlit Cloud Deployment

### Prerequisites

- [ ] **GitHub repository created**
  ```bash
  git init
  git add .
  git commit -m "Initial commit for Streamlit"
  ```

- [ ] **Repository is public or accessible**
  - Streamlit Cloud needs access
  - Or configure private repo access

- [ ] **Main file is named correctly**
  - File is `streamlit_app.py` at root level
  - Or update Streamlit Cloud settings

### LLM Backend Decision

Choose one option:

**Option A: Hosted Ollama**
- [ ] Ollama deployed on cloud server (AWS/DigitalOcean/etc.)
- [ ] Server is publicly accessible with proper security
- [ ] URL updated in `.streamlit/secrets.toml`
- [ ] Tested connection from external network

**Option B: Cloud LLM Service (Recommended)** ⭐
- [ ] OpenAI API key obtained
- [ ] OR Anthropic/other LLM service configured
- [ ] Code updated to use cloud LLM (see STREAMLIT_DEPLOYMENT.md)
- [ ] API key added to Streamlit secrets (not committed!)
- [ ] Dependencies updated (add `openai` to requirements.txt)

### Streamlit Cloud Setup

- [ ] **Sign in to Streamlit Cloud**
  - Visit [share.streamlit.io](https://share.streamlit.io)
  - Connect GitHub account

- [ ] **Create new app**
  - Click "New app"
  - Select your repository
  - Branch: `main` (or your default branch)
  - Main file: `streamlit_app.py`

- [ ] **Configure secrets**
  - Go to app settings → Secrets
  - Add your secrets from `.streamlit/secrets.toml`
  - Example for OpenAI:
    ```toml
    [openai]
    api_key = "sk-..."
    use_openai = true
    ```

- [ ] **Deploy and monitor**
  - Click "Deploy"
  - Watch logs for errors
  - Wait for "Your app is live!" message

- [ ] **Test deployed app**
  - Upload test transcript
  - Verify processing works
  - Check all features functional

## 🔒 Security Checklist

- [ ] **Secrets not committed**
  - `.streamlit/secrets.toml` in `.gitignore`
  - No API keys in code
  - Environment variables used properly

- [ ] **File validation enabled**
  - Only .txt files accepted
  - File size limits enforced
  - Content sanitization in place

- [ ] **Dependencies up to date**
  ```bash
  pip list --outdated
  ```

- [ ] **HTTPS enabled**
  - Streamlit Cloud provides this automatically
  - For custom hosting, ensure SSL certificate

## 📊 Performance Checklist

- [ ] **Resource limits understood**
  - Streamlit Cloud free tier: 1GB RAM
  - Processing timeout: ~10 minutes max
  - Consider upgrading for production

- [ ] **Large file handling**
  - Tested with max size file (10MB)
  - Timeout handling implemented
  - User feedback during processing

- [ ] **Caching implemented** (if needed)
  - Use `@st.cache_data` for expensive ops
  - Clear cache strategy defined

## 🎨 UI/UX Checklist

- [ ] **Theme configured**
  - `.streamlit/config.toml` customized
  - Colors match brand (if applicable)
  - Responsive on mobile tested

- [ ] **User feedback clear**
  - Progress indicators work
  - Error messages helpful
  - Success confirmations present

- [ ] **Instructions visible**
  - Sidebar help text clear
  - Upload instructions obvious
  - Format requirements stated

## 📝 Documentation Checklist

- [ ] **README updated**
  - Deployment section accurate
  - Links work correctly
  - Prerequisites listed

- [ ] **Usage guide available**
  - QUICKSTART_STREAMLIT.md complete
  - Example transcripts provided
  - Troubleshooting section helpful

- [ ] **Deployment guide complete**
  - STREAMLIT_DEPLOYMENT.md accurate
  - Both local and cloud covered
  - LLM alternatives documented

## 🧪 Testing Checklist

### Functional Tests

- [ ] **Upload workflow**
  - File picker works
  - Valid files accepted
  - Invalid files rejected

- [ ] **Processing workflow**
  - Progress shown correctly
  - No timeout on normal transcripts
  - Errors handled gracefully

- [ ] **Results display**
  - All tabs populate
  - Data formatted correctly
  - No missing information

- [ ] **Download feature**
  - JSON file valid
  - Filename includes timestamp
  - Content complete

### Edge Cases

- [ ] **Empty file**
  - Handled with clear message

- [ ] **Large file (>10MB)**
  - Rejected with size error

- [ ] **Non-UTF-8 encoding**
  - Error message displayed

- [ ] **No speakers in transcript**
  - Fallback parser works
  - Results still generated

- [ ] **Network error (LLM)**
  - Timeout handled
  - Error message clear
  - Retry suggested

### Browser Compatibility

- [ ] Chrome/Edge tested
- [ ] Firefox tested
- [ ] Safari tested (if Mac available)
- [ ] Mobile browser tested

## 🚀 Go-Live Checklist

### Just Before Launch

- [ ] **Final local test**
  ```bash
  streamlit run streamlit_app.py
  ```

- [ ] **Final git push**
  ```bash
  git status  # Verify nothing sensitive
  git add .
  git commit -m "Ready for deployment"
  git push origin main
  ```

- [ ] **Streamlit Cloud redeploy**
  - Trigger deployment
  - Watch logs carefully
  - Verify app comes up

- [ ] **Production smoke test**
  - Visit deployed URL
  - Upload test transcript
  - Verify end-to-end flow
  - Download results

### Post-Launch

- [ ] **Monitor logs**
  - Check Streamlit Cloud logs
  - Watch for errors
  - Review usage patterns

- [ ] **Share URL**
  - App URL: `https://your-app.streamlit.app`
  - Share with team/users
  - Document in appropriate places

- [ ] **Set up monitoring** (optional)
  - Error tracking
  - Usage analytics
  - Performance monitoring

## 📞 Support Preparation

- [ ] **Known issues documented**
  - Common problems listed
  - Solutions provided
  - Workarounds noted

- [ ] **Contact method decided**
  - GitHub issues
  - Email support
  - Slack/Discord channel

- [ ] **Escalation path defined**
  - Who handles what
  - Response time goals
  - Critical issue process

## ✅ Final Verification

Before marking deployment complete:

- [ ] App is live and accessible
- [ ] Test transcript processes successfully
- [ ] All features work as expected
- [ ] No errors in logs
- [ ] Performance is acceptable
- [ ] Documentation is accurate
- [ ] Team/users have access
- [ ] Support channels ready

## 🎉 Success!

Once all items are checked:

✅ **Your ClarifyMeet AI app is deployed!**

Share your app URL: `https://your-app-name.streamlit.app`

---

## 📚 Quick Reference

**Local Test:**
```bash
streamlit run streamlit_app.py
```

**Deploy to Cloud:**
1. Push to GitHub
2. Connect at share.streamlit.io
3. Configure secrets
4. Deploy!

**Troubleshooting:**
- See `STREAMLIT_DEPLOYMENT.md`
- Check `TESTING.md`
- Review logs in Streamlit Cloud dashboard

---

**Questions?** Review the documentation:
- README.md
- QUICKSTART_STREAMLIT.md
- STREAMLIT_DEPLOYMENT.md
- MIGRATION_SUMMARY.md

Good luck! 🚀
