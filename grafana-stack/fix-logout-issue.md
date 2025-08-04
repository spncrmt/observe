# Fix Grafana Auto-Logout Issue

## 🎯 **Problem**
You keep getting auto-logged out of Grafana due to session timeout or cookie issues.

## ✅ **Solutions Applied**

### **1. Updated Grafana Configuration**
- **Session lifetime:** 24 hours (86400 seconds)
- **Remember me duration:** 7 days (604800 seconds)
- **Cookie settings:** Fixed for HTTPS domain
- **SameSite:** Changed from `strict` to `none`

### **2. Browser Cache/Cookie Fix**

**Chrome/Edge:**
1. **Open Developer Tools** (F12)
2. **Go to Application/Storage tab**
3. **Clear Storage:**
   - Click "Clear storage"
   - Check all boxes
   - Click "Clear site data"
4. **Clear Cookies:**
   - Go to Settings → Privacy → Clear browsing data
   - Select "Cookies and other site data"
   - Click "Clear data"

**Firefox:**
1. **Go to Settings → Privacy & Security**
2. **Click "Clear Data"**
3. **Check "Cookies and Site Data"**
4. **Click "Clear"**

### **3. Manual Cookie Check**
1. **Go to** `https://awtospx.com`
2. **Open Developer Tools** (F12)
3. **Go to Application → Cookies**
4. **Look for `grafana_session` cookie**
5. **If it exists, delete it and refresh**

### **4. Alternative: Use Incognito/Private Mode**
- **Open incognito/private window**
- **Go to** `https://awtospx.com`
- **Login with admin/admin**
- **Test if logout still occurs**

## 🔧 **Deployment Update**

The configuration has been updated in:
- `grafana-stack/Dockerfile.grafana`
- `grafana-stack/grafana/grafana.ini`
- `render.yaml`

**Next deployment will include these fixes.**

## 🎯 **Quick Test**

1. **Clear browser cache/cookies**
2. **Go to** `https://awtospx.com`
3. **Login with admin/admin**
4. **Wait 5 minutes** - should not auto-logout
5. **Refresh page** - should stay logged in

## 🚨 **If Still Logging Out**

**Check these settings in Grafana:**
1. **Go to** Configuration → Preferences
2. **Check "Remember me"** is enabled
3. **Set session timeout** to 24 hours
4. **Save settings**

**Contact support if issue persists!** 