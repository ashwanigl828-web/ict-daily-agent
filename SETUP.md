# 📚 ICT Daily PDF Agent — सम्पूर्ण Setup Guide

> **🎯 यह guide एक school teacher के लिए लिखी गई है जिन्हें coding नहीं आती।**
> **हर step बिल्कुल detail में समझाया गया है। बस step-by-step follow करें!**

---

## 📖 विषय-सूची (Table of Contents)

1. [🤔 यह System क्या है?](#-यह-system-क्या-है)
2. [📋 शुरू करने से पहले (Prerequisites)](#-शुरू-करने-से-पहले-prerequisites)
3. [Step 1: GitHub Account बनाएं](#step-1--github-account-बनाएं-free)
4. [Step 2: Gemini API Key लें](#step-2--gemini-api-key-लें-free)
5. [Step 3: Meta Developer Account बनाएं (WhatsApp API)](#step-3--meta-developer-account-बनाएं-whatsapp-api---free)
6. [Step 4: Supabase Account बनाएं (Database)](#step-4--supabase-account-बनाएं-free-database)
7. [Step 5: Cloudinary Account बनाएं (File Storage)](#step-5--cloudinary-account-बनाएं-free-file-storage)
8. [Step 6: Project को GitHub पर Upload करें](#step-6--project-को-github-पर-upload-करें)
9. [Step 7: Render.com पर Deploy करें](#step-7--rendercom-पर-deploy-करें-free---247-online)
10. [Step 8: GitHub Actions Setup करें](#step-8--github-actions-setup-करें-daily-auto-run)
11. [Step 9: WhatsApp पर Students को Setup करें](#step-9--whatsapp-पर-students-को-setup-करें)
12. [Step 10: Testing करें](#step-10--testing-करें-)
13. [🔧 समस्या समाधान (Troubleshooting)](#-समस्या-समाधान-troubleshooting)
14. [💰 Free Tier Limits](#-free-tier-limits)
15. [📞 मदद चाहिए?](#-मदद-चाहिए)

---

## 🤔 यह System क्या है?

**सरल भाषा में:** यह system **हर रोज़ सुबह 8 बजे** automatically एक PDF बनाता है जिसमें आज का topic होता है — AI (Artificial Intelligence) की मदद से। फिर यह PDF **WhatsApp** पर students को भेज देता है। शाम को students एक form भरते हैं कि उन्होंने कितना समझा। आप **dashboard** पर सब कुछ देख सकते हैं।

### 🔄 Daily Flow (रोज़ क्या होता है):

```
सुबह 8:00 AM
    ↓
🤖 AI नया topic चुनता है (Google Gemini)
    ↓
📄 सुंदर PDF बनता है (Hindi/English में)
    ↓
☁️ PDF cloud पर upload होता है (Cloudinary)
    ↓
📱 WhatsApp पर students को भेजा जाता है
    ↓
🌙 शाम को students form भरते हैं
    ↓
📊 Teacher dashboard पर results देखते हैं
```

### 🆓 सब कुछ FREE है!

| Service | क्या करता है | Free Limit |
|---------|-------------|------------|
| GitHub | Code store करता है | ♾️ Unlimited |
| Google Gemini | AI से content बनाता है | 60 requests/min |
| WhatsApp Cloud API | Messages भेजता है | 1,000/month |
| Supabase | Database (data store) | 500 MB |
| Cloudinary | PDF files store करता है | 25 GB |
| Render.com | App को 24/7 चलाता है | 750 hours/month |
| GitHub Actions | Daily schedule चलाता है | 2,000 min/month |

> **💡 एक class के 40-50 students के लिए यह सब free limits काफी हैं!**

---

## 📋 शुरू करने से पहले (Prerequisites)

### आपको चाहिए:

| # | चीज़ | क्यों ज़रूरी है |
|---|------|----------------|
| 1 | 📱 Mobile phone with WhatsApp | Students को PDF भेजने के लिए |
| 2 | 💻 Computer/Laptop with Internet | Account बनाने और setup करने के लिए |
| 3 | 📧 Email ID (Gmail recommended) | सभी accounts बनाने के लिए |
| 4 | 📞 Phone number (for WhatsApp Business) | WhatsApp API के लिए |
| 5 | ⏰ 2-3 घंटे का समय | पूरा setup करने के लिए |

### ⚠️ ज़रूरी बातें:
- **सभी passwords एक diary में लिख लें** — बाद में ज़रूरत पड़ेगी
- **API keys को कभी किसी को न बताएं** — ये आपके account की चाबियां हैं
- **एक-एक step carefully follow करें** — कोई step skip न करें

---

## Step 1: 🐙 GitHub Account बनाएं (Free)

### 📌 GitHub क्या है?
GitHub एक website है जहाँ हम अपना code (project files) store करते हैं। यह Google Drive जैसा है, लेकिन code के लिए। हमारा daily PDF system का सारा code यहीं रहेगा।

### 📝 Step-by-Step:

**1.1)** Browser खोलें (Chrome/Edge) और जाएं: **https://github.com**

**1.2)** **"Sign up"** button पर click करें (ऊपर दाईं तरफ)

**1.3)** अपनी details भरें:
   - **Email:** अपना Gmail डालें (example: `teacher.sharma@gmail.com`)
   - **Password:** एक strong password बनाएं (8+ characters, number + letter)
     - 💡 Example: `MySchool@2024` (इसे diary में लिख लें!)
   - **Username:** एक unique name चुनें (example: `sharma-teacher-school`)
     - ⚠️ यह name दूसरों को दिखेगा, decent name रखें

**1.4)** **"Create account"** पर click करें

**1.5)** Email verification:
   - अपना Gmail खोलें
   - GitHub से आया email ढूंढें ("Please verify your email address")
   - Email में दिया गया **verification code** (6 अंकों का number) copy करें
   - GitHub पर वापस जाकर code paste करें

**1.6)** कुछ questions आएंगे (optional):
   - "How many team members?" → **Just me**
   - "What features are you interested in?" → कुछ भी select करें या **Skip** करें
   - Plan select करें → **Free** (Continue for free)

### ✅ कैसे verify करें कि सही हुआ:
- ✅ आप https://github.com पर login हो गए हैं
- ✅ ऊपर दाईं तरफ आपका profile icon दिख रहा है
- ✅ Dashboard page दिख रहा है

### 📸 कैसा दिखेगा:
> GitHub Dashboard पर आपको "Start a new repository" का option दिखेगा, एक green button होगा। अभी कुछ न करें, आगे बढ़ें।

---

## Step 2: 🤖 Gemini API Key लें (Free)

### 📌 Gemini API Key क्या है?
Google Gemini एक AI है (ChatGPT जैसा)। API Key एक "password" जैसी चीज़ है जो हमारे app को Gemini AI से बात करने देती है। इसी AI से हमारा system daily topics का content बनाएगा।

### 📝 Step-by-Step:

**2.1)** Browser में जाएं: **https://aistudio.google.com**

**2.2)** **"Sign in"** करें अपने Google/Gmail account से
   - वही Gmail use करें जो आपने Step 1 में use किया था
   - अगर already Gmail में login हैं तो automatically sign in हो जाएगा

**2.3)** AI Studio का dashboard खुलेगा। बाएं तरफ menu में **"Get API key"** पर click करें
   - 💡 अगर "Get API key" नहीं दिखे, तो ऊपर URL bar में सीधे जाएं: **https://aistudio.google.com/apikey**

**2.4)** **"Create API key"** button पर click करें (blue button)

**2.5)** एक popup आएगा:
   - "Select Google Cloud project" — **"Create API key in new project"** select करें
   - **"Create API key"** पर click करें

**2.6)** 🔑 आपकी API Key बन गई! यह कुछ इस तरह दिखेगी:
   ```
   AIzaSyD_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   - **"Copy"** button पर click करें
   - 📝 **इसे तुरंत Notepad में paste करें और save करें!**
   - File name रखें: `my-api-keys.txt`

### ⚠️ सावधानी:
- ❌ यह key किसी को न भेजें (WhatsApp, email पर भी नहीं)
- ❌ इसे social media पर post न करें
- ✅ बस Notepad file में सुरक्षित रखें

### ✅ कैसे verify करें:
- ✅ API Key `AIza` से शुरू होती है
- ✅ Key Notepad file में save हो गई
- ✅ Google AI Studio पर "API keys" section में आपकी key दिख रही है

### 🧪 Test करें (Optional):
- AI Studio पर बाएं menu में **"Prompts"** पर जाएं
- Text box में लिखें: `Hello, write a short poem about learning`
- **Run** पर click करें — अगर AI ने जवाब दिया तो सब सही है!

---

## Step 3: 📱 Meta Developer Account बनाएं (WhatsApp API - Free)

### 📌 WhatsApp Cloud API क्या है?
यह Meta (Facebook) की service है जो हमें program से WhatsApp messages भेजने देती है। इसी से PDF students को WhatsApp पर पहुंचेगी। **पहले 1,000 conversations हर month free हैं!**

### ⚠️ Important: इस step में कई sub-steps हैं। ध्यान से follow करें!

---

### 📝 Part A: Developer Account बनाएं

**3.1)** Browser में जाएं: **https://developers.facebook.com**

**3.2)** **"Get Started"** या **"Log In"** button पर click करें

**3.3)** अपने **Facebook account** से login करें
   - 💡 अगर Facebook account नहीं है, तो पहले https://www.facebook.com पर जाकर बनाएं
   - Personal Facebook account भी चलेगा

**3.4)** Developer registration form भरें:
   - ✅ Terms and conditions accept करें
   - **"Register"** पर click करें
   - Email verify करें (Facebook से आए email में link click करें)

**3.5)** Account type select करें:
   - अगर पूछे तो **"Developer"** select करें
   - **"Complete Registration"** पर click करें

### ✅ Verify: आप https://developers.facebook.com/apps/ पर पहुंच गए

---

### 📝 Part B: New App बनाएं

**3.6)** **"Create App"** button पर click करें (green button, ऊपर दाईं तरफ)

**3.7)** App details भरें:
   - **"What do you want your app to do?"** → **"Other"** select करें → **Next**
   - **App type:** **"Business"** select करें → **Next**
   - **App name:** `ICT Daily Agent` (या कोई भी नाम)
   - **App contact email:** अपना email
   - **Business portfolio:** अगर पूछे तो "I don't want to connect..." select करें या skip करें
   - **"Create app"** पर click करें

**3.8)** Facebook password दोबारा डालें (security check)

**3.9)** App Dashboard खुलेगा। यहाँ बहुत सारे products दिखेंगे।

**3.10)** **"WhatsApp"** ढूंढें और उसके नीचे **"Set up"** पर click करें
   - 💡 अगर WhatsApp दिखाई न दे, तो scroll down करें या search box में "WhatsApp" type करें

**3.11)** अगर Business portfolio बनाने को कहे:
   - **"Continue"** पर click करें
   - एक Meta Business Portfolio automatically बन जाएगा

### ✅ Verify: बाएं menu में "WhatsApp" section दिख रहा है

---

### 📝 Part C: WhatsApp API Setup — Test Number और Token लें

**3.12)** बाएं menu में जाएं: **WhatsApp → API Setup**

**3.13)** इस page पर आपको दो important चीज़ें मिलेंगी:

**📞 Test Phone Number:**
   - "From" section में एक phone number दिखेगा (यह Meta का test number है)
   - इसके नीचे **"Phone number ID"** लिखा होगा — कुछ इस तरह:
     ```
     Phone number ID: 1234567890123456
     ```
   - 📝 इसे copy करें और Notepad file (`my-api-keys.txt`) में लिखें:
     ```
     WHATSAPP_PHONE_NUMBER_ID = 1234567890123456
     ```

**🔑 Temporary Access Token:**
   - "Temporary access token" section में एक लंबा token दिखेगा
   - ⚠️ **यह token सिर्फ 24 घंटे valid है!** — बाद में हम permanent token बनाएंगे
   - अभी के लिए copy करके Notepad में save करें:
     ```
     WHATSAPP_TOKEN (TEMPORARY) = EAAxxxxxxxxxxxxxxx...
     ```

---

### 📝 Part D: Test Message भेजें (verify करने के लिए)

**3.14)** उसी API Setup page पर नीचे scroll करें

**3.15)** **"To"** section में:
   - **"Manage phone number list"** पर click करें
   - अपना personal WhatsApp number add करें (जिस पर test message आएगा)
   - Country code select करें: **India (+91)**
   - Number डालें (बिना +91 के, जैसे: `9876543210`)
   - **"Add"** पर click करें
   - WhatsApp पर एक verification code आएगा — उसे enter करें

**3.16)** अब **"Send message"** button पर click करें

**3.17)** 📱 अपना WhatsApp check करें — एक test message आना चाहिए!
   - Message कुछ ऐसा होगा: "Hello World" from an unknown number

### ✅ Verify: WhatsApp पर test message आ गया ✅

---

### 📝 Part E: Permanent Access Token बनाएं (बहुत Important! ⭐)

> ⚠️ **Temporary token सिर्फ 24 घंटे चलता है।** Daily system के लिए हमें **permanent token** चाहिए। नीचे दिए steps carefully follow करें:

**3.18)** Browser में जाएं: **https://business.facebook.com/settings/**
   - 💡 या: developers.facebook.com → ऊपर अपने app name पर click → **Business Settings**

**3.19)** बाईं तरफ menu में, **"Users"** section ढूंढें → **"System users"** पर click करें

**3.20)** **"Add"** button पर click करें:
   - **System user name:** `ict-daily-bot`
   - **Role:** **Admin**
   - **"Create system user"** पर click करें

**3.21)** अब इस system user को app access दें:
   - बने हुए `ict-daily-bot` user पर click करें
   - **"Add Assets"** पर click करें
   - **"Apps"** tab select करें
   - अपना app (`ICT Daily Agent`) select करें
   - ✅ **"Full Control"** toggle ON करें
   - **"Save Changes"** पर click करें

**3.22)** WhatsApp account भी assign करें:
   - फिर से **"Add Assets"** पर click करें
   - इस बार **"WhatsApp Accounts"** tab select करें
   - अपना WhatsApp Business Account select करें
   - ✅ **"Full Control"** toggle ON करें
   - **"Save Changes"** पर click करें

**3.23)** अब Permanent Token generate करें:
   - `ict-daily-bot` user पर click करें
   - **"Generate new token"** button पर click करें
   - अपना app (`ICT Daily Agent`) select करें
   - **Token expiration:** **"Never"** select करें ⭐
   - **Permissions** में ये select करें (checkbox tick करें):
     - ✅ `whatsapp_business_messaging`
     - ✅ `whatsapp_business_management`
   - **"Generate token"** पर click करें

**3.24)** 🔑 **Permanent Token** दिखेगा! 
   - **तुरंत copy करें!** (यह दोबारा नहीं दिखेगा!)
   - Notepad file में save करें:
     ```
     WHATSAPP_TOKEN (PERMANENT) = EAAxxxxxxxx....(बहुत लंबा token)....xxxxx
     ```
   - ⚠️ **इस token को बहुत संभाल कर रखें — यह आपके WhatsApp account की master key है!**

---

### 📝 Part F: WhatsApp Message Template बनाएं

> WhatsApp API में पहले message भेजने के लिए **approved template** ज़रूरी होता है।

**3.25)** जाएं: **WhatsApp → Message Templates** (बाएं menu में, या directly: https://business.facebook.com/wa/manage/message-templates/)

**3.26)** **"Create Template"** पर click करें

**3.27)** Template 1 — Daily PDF भेजने के लिए:
   - **Category:** `Utility`
   - **Name:** `daily_study_material` (सिर्फ lowercase और underscore)
   - **Language:** `Hindi (hi)` — Add language: `English (en)` भी add करें
   - **"Continue"** पर click करें

**3.28)** Template content design करें:

   **Header (optional):**
   - Type: **Document** (क्योंकि हम PDF भेजेंगे)

   **Body:**
   ```
   📚 आज का Study Material

   विषय: {{1}}
   कक्षा: {{2}}
   दिनांक: {{3}}

   ऊपर दी गई PDF ध्यान से पढ़ें और शाम तक feedback form भरें।

   🔗 Feedback Form: {{4}}

   📖 पढ़ाई में मज़ा आए! 🌟
   ```
   
   - `{{1}}`, `{{2}}`, `{{3}}`, `{{4}}` — ये variables हैं जो हर message में बदलेंगे

   **Footer (optional):**
   ```
   ICT Daily Learning System
   ```

   **Buttons (optional):**
   - Type: **URL**
   - Button text: `Form भरें`
   - URL: `{{1}}` (variable URL)

**3.29)** **"Submit"** पर click करें

**3.30)** ⏰ Template approval में **कुछ मिनट से लेकर 24 घंटे** लग सकते हैं
   - Status: **Pending** → review हो रहा है
   - Status: **Approved** ✅ → use कर सकते हैं
   - Status: **Rejected** ❌ → content बदलकर फिर submit करें

### ✅ Final WhatsApp Verify Checklist:
- ✅ Developer account बन गया
- ✅ App बन गया with WhatsApp product
- ✅ Phone Number ID note कर लिया
- ✅ **Permanent** Access Token बना लिया और save कर लिया
- ✅ Test message अपने WhatsApp पर आ गया
- ✅ Message template submit हो गया

---

## Step 4: 🗄️ Supabase Account बनाएं (Free Database)

### 📌 Supabase क्या है?
Supabase एक **free database** service है। Database = organized data storage (Excel sheet जैसा लेकिन powerful)। इसमें हम store करेंगे:
- कौन से topics भेजे गए
- Students ने क्या feedback दिया
- AI के suggestions

### 📝 Step-by-Step:

**4.1)** Browser में जाएं: **https://supabase.com**

**4.2)** **"Start your project"** या **"Sign Up"** पर click करें

**4.3)** **"Sign in with GitHub"** पर click करें (सबसे आसान तरीका!)
   - 💡 Step 1 में बनाए GitHub account से login करें
   - GitHub permission page आएगा → **"Authorize Supabase"** पर click करें

**4.4)** Supabase Dashboard खुलेगा

**4.5)** **"New Project"** button पर click करें (green button)

**4.6)** Project details भरें:
   - **Organization:** अगर पूछे तो new organization बनाएं (कोई भी नाम, जैसे: `my-school`)
   - **Project name:** `ict-daily-agent`
   - **Database Password:** एक strong password डालें
     - 💡 Example: `Supabase@School2024`
     - 📝 **इसे ज़रूर Notepad में save करें!**
   - **Region:** `South Asia (Mumbai)` select करें — India से closest है
   - **Plan:** **Free** (already selected होगा)
   - **"Create new project"** पर click करें

**4.7)** ⏰ Project बनने में 1-2 minute लगेंगे। Wait करें जब तक green status न दिखे।

---

### 📝 Part B: Database Tables बनाएं (SQL commands)

> अब हम database में tables बनाएंगे — जैसे Excel sheets बनाते हैं।

**4.8)** बाएं menu में **"SQL Editor"** पर click करें (icon: `</>`)

**4.9)** **"New query"** पर click करें

**4.10)** नीचे दिया गया **पूरा SQL code** copy करें और SQL Editor में paste करें:

```sql
-- ============================================================
-- ICT Daily Agent — Database Tables
-- ============================================================
-- इस पूरे code को copy करके SQL Editor में paste करें
-- फिर "Run" button पर click करें
-- ============================================================

-- 📚 Table 1: Topic History (कौन सा topic कब भेजा गया)
CREATE TABLE IF NOT EXISTS topic_history (
    id BIGSERIAL PRIMARY KEY,
    topic_name TEXT NOT NULL,
    class_standard TEXT NOT NULL,
    category TEXT,
    part_number INTEGER DEFAULT 1,
    total_parts INTEGER DEFAULT 1,
    pdf_path TEXT,
    pdf_url TEXT,
    sent_date DATE DEFAULT CURRENT_DATE,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_topic_history_date ON topic_history(sent_date);
CREATE INDEX IF NOT EXISTS idx_topic_history_class ON topic_history(class_standard);

-- 📝 Table 2: Student Responses (Students का feedback)
CREATE TABLE IF NOT EXISTS student_responses (
    id BIGSERIAL PRIMARY KEY,
    student_name TEXT NOT NULL,
    student_phone TEXT,
    class_standard TEXT NOT NULL,
    topic_name TEXT NOT NULL,
    has_read BOOLEAN DEFAULT FALSE,
    understanding_level TEXT CHECK (understanding_level IN ('easy', 'medium', 'hard', 'not_understood')),
    difficult_part TEXT,
    quiz_answers TEXT,
    quiz_score INTEGER DEFAULT 0,
    additional_feedback TEXT,
    response_date DATE DEFAULT CURRENT_DATE,
    responded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_responses_date ON student_responses(response_date);
CREATE INDEX IF NOT EXISTS idx_responses_class ON student_responses(class_standard);
CREATE INDEX IF NOT EXISTS idx_responses_topic ON student_responses(topic_name);

-- 📊 Table 3: Improvement Log (AI के suggestions)
CREATE TABLE IF NOT EXISTS improvement_log (
    id BIGSERIAL PRIMARY KEY,
    topic_name TEXT NOT NULL,
    class_standard TEXT NOT NULL,
    total_responses INTEGER DEFAULT 0,
    avg_understanding FLOAT,
    avg_quiz_score FLOAT,
    common_difficulties TEXT,
    ai_suggestions TEXT,
    action_taken TEXT,
    log_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_improvement_date ON improvement_log(log_date);

-- 📋 Table 4: WhatsApp Contacts (Students की list)
CREATE TABLE IF NOT EXISTS whatsapp_contacts (
    id BIGSERIAL PRIMARY KEY,
    student_name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    class_standard TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    opted_in_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_contacts_class ON whatsapp_contacts(class_standard);
CREATE INDEX IF NOT EXISTS idx_contacts_active ON whatsapp_contacts(is_active);

-- ✅ Tables बन गए!
-- अब आप ऊपर "Table Editor" में जाकर देख सकते हैं
```

**4.11)** **"Run"** button पर click करें (▶️ play button, या Ctrl+Enter)

**4.12)** नीचे "Success. No rows returned" message आएगा — **यह सही है!** ✅

**4.13)** Verify करें: बाएं menu में **"Table Editor"** पर click करें
   - आपको 4 tables दिखनी चाहिए:
     - ✅ `topic_history`
     - ✅ `student_responses`
     - ✅ `improvement_log`
     - ✅ `whatsapp_contacts`

---

### 📝 Part C: API Keys copy करें

**4.14)** बाएं menu में **"Settings"** (⚙️ gear icon) पर click करें

**4.15)** **"API"** section पर click करें (under "Configuration")

**4.16)** यहाँ दो important चीज़ें मिलेंगी:

**🔗 Project URL:**
   ```
   https://xxxxxxxxxxxx.supabase.co
   ```
   - Copy करें और Notepad में save करें:
     ```
     SUPABASE_URL = https://xxxxxxxxxxxx.supabase.co
     ```

**🔑 Project API Key (anon / public):**
   - "anon" key copy करें (यह `eyJhbGci...` से शुरू होगी)
   - Notepad में save करें:
     ```
     SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxx
     ```
   - ⚠️ "service_role" key **मत copy करें** — "anon" key ही use करें

### ✅ Verify:
- ✅ 4 tables बन गए (Table Editor में दिख रहे हैं)
- ✅ Project URL save हो गया
- ✅ API Key (anon) save हो गया

---

## Step 5: 🌤️ Cloudinary Account बनाएं (Free File Storage)

### 📌 Cloudinary क्या है?
Cloudinary एक **cloud storage** service है (Google Drive जैसी)। हम generated PDF files यहाँ upload करेंगे ताकि WhatsApp पर link भेज सकें। **25 GB free storage** मिलती है!

### 📝 Step-by-Step:

**5.1)** Browser में जाएं: **https://cloudinary.com**

**5.2)** **"Sign Up for Free"** पर click करें

**5.3)** Registration form भरें:
   - **Name:** अपना नाम
   - **Email:** अपना email
   - **Password:** एक password बनाएं
   - **Cloud name:** कुछ भी रखें (example: `ict-daily-school`) — या auto-generated accept करें
   - ✅ Terms accept करें
   - **"Create Account"** पर click करें

**5.4)** Email verification:
   - अपना email खोलें
   - Cloudinary से आया email ढूंढें
   - **"Verify Email"** link/button पर click करें

**5.5)** कुछ survey questions आ सकते हैं — Skip करें या कुछ भी select करें

**5.6)** 🎉 Cloudinary Dashboard खुलेगा!

**5.7)** Dashboard पर **तीन important values** दिखेंगी:

   ```
   Cloud name:    ict-daily-school
   API Key:       123456789012345
   API Secret:    abcDefGHijklMNOpqrSTUvwxyz
   ```

   📝 तीनों को copy करके Notepad file में save करें:
   ```
   CLOUDINARY_CLOUD_NAME = ict-daily-school
   CLOUDINARY_API_KEY = 123456789012345
   CLOUDINARY_API_SECRET = abcDefGHijklMNOpqrSTUvwxyz
   ```

   - 💡 **"API Secret"** दिखाने के लिए 👁️ (eye) icon पर click करना पड़ सकता है

### ✅ Verify:
- ✅ Cloudinary Dashboard खुल रहा है
- ✅ Cloud Name, API Key, API Secret तीनों note कर लिए

---

## Step 6: 📤 Project को GitHub पर Upload करें

### 📌 अब हम project files को GitHub पर upload करेंगे

> GitHub पर files upload करने के **2 तरीके** हैं। **तरीका A (आसान)** recommended है अगर आपको Git नहीं आता।

---

### 🅰️ तरीका A: GitHub Website से Upload करें (आसान — No coding!)

**6.1)** GitHub पर जाएं: **https://github.com** (login करें)

**6.2)** **"+"** icon पर click करें (ऊपर दाईं तरफ) → **"New repository"**

**6.3)** Repository details:
   - **Repository name:** `ict-daily-agent`
   - **Description:** `Daily PDF study material system for students via WhatsApp`
   - **Public** select करें (Free tier में public ज़रूरी है)
   - ✅ **"Add a README file"** checkbox tick करें
   - ✅ **Add .gitignore** → template: **Python** select करें
   - **"Create repository"** पर click करें

**6.4)** Repository बन गया! अब files upload करें:
   - **"Add file"** button पर click करें → **"Upload files"**
   - अपने computer से project की **सभी files** drag करें या **"choose your files"** पर click करें
   - ⚠️ `.env` file upload **न करें!** (इसमें secret keys हैं)
   - ये files upload करें:
     - `app.py`
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
     - `render.yaml`
     - `templates/` folder (सारी HTML files)
     - `agents/` folder
     - `utils/` folder
     - `.github/workflows/daily_pdf.yml`
     - और बाकी सभी project files

**6.5)** नीचे "Commit changes" section में:
   - Message: `Initial upload - all project files`
   - **"Commit changes"** button पर click करें

**6.6)** ⏰ Upload होने में कुछ seconds लगेंगे

### ✅ Verify:
- ✅ GitHub repository page पर सारी files दिख रही हैं
- ✅ `.github/workflows/daily_pdf.yml` file दिख रही है
- ✅ `app.py`, `requirements.txt`, `Procfile` दिख रहे हैं

---

### 🅱️ तरीका B: Git Commands से Upload करें (Advanced)

> यह तरीका तभी use करें जब आपके computer में **Git** installed है

**6.1)** Git install करें (अगर नहीं है):
   - Download: https://git-scm.com/downloads
   - Install करें (सब default settings रखें)

**6.2)** Command Prompt (CMD) या PowerShell खोलें

**6.3)** Project folder में जाएं:
   ```bash
   cd C:\Users\ashwa\.gemini\antigravity\scratch\ict-daily-agent
   ```

**6.4)** Git commands चलाएं (एक-एक करके):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ICT Daily Agent"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ict-daily-agent.git
   git push -u origin main
   ```
   - ⚠️ `YOUR_USERNAME` की जगह अपना GitHub username डालें!
   - GitHub login popup आएगा → login करें

### ✅ Verify (दोनों तरीकों के लिए):
- ✅ `https://github.com/YOUR_USERNAME/ict-daily-agent` पर सारी files दिख रही हैं

---

## Step 7: 🚀 Render.com पर Deploy करें (Free - 24/7 Online)

### 📌 Render.com क्या है?
Render.com एक service है जो हमारे app को internet पर 24/7 चलाती है। जैसे दुकान खोलने के लिए जगह चाहिए, वैसे ही app चलाने के लिए server चाहिए। Render **free** में server देता है!

### 📝 Step-by-Step:

**7.1)** Browser में जाएं: **https://render.com**

**7.2)** **"Get Started for Free"** पर click करें

**7.3)** **"GitHub"** से sign up करें (recommended!)
   - GitHub permission page → **"Authorize Render"** पर click करें
   - 💡 इससे Render automatically आपके GitHub repos access कर सकेगा

**7.4)** Render Dashboard खुलेगा

**7.5)** **"New +"** button पर click करें (ऊपर) → **"Web Service"** select करें

**7.6)** **"Build and deploy from a Git repository"** select करें → **Next**

**7.7)** अपना `ict-daily-agent` repository ढूंढें:
   - अगर repository दिखे → **"Connect"** पर click करें
   - अगर न दिखे → **"Configure account"** पर click करें:
     - GitHub permissions page खुलेगा
     - **"All repositories"** select करें (या specifically `ict-daily-agent`)
     - **"Save"** पर click करें
     - वापस Render पर आकर repository select करें

**7.8)** Service settings भरें:

   | Setting | Value |
   |---------|-------|
   | **Name** | `ict-daily-agent` |
   | **Region** | `Singapore (Southeast Asia)` — India से closest |
   | **Branch** | `main` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2` |
   | **Plan** | **Free** ⭐ |

**7.9)** 🔐 **Environment Variables** add करें — यह सबसे important step है!

   **"Advanced"** section expand करें → **"Add Environment Variable"** पर click करें

   एक-एक करके ये सभी variables add करें (Notepad file से values copy करें):

   | Key | Value (Notepad से copy करें) |
   |-----|------|
   | `GEMINI_API_KEY` | `AIzaSy....` (Step 2 से) |
   | `WHATSAPP_TOKEN` | `EAA....` (Step 3, Permanent Token) |
   | `WHATSAPP_PHONE_NUMBER_ID` | `12345...` (Step 3 से) |
   | `WHATSAPP_VERIFY_TOKEN` | कोई भी secret word, जैसे: `my_school_verify_2024` |
   | `SUPABASE_URL` | `https://xxx.supabase.co` (Step 4 से) |
   | `SUPABASE_KEY` | `eyJhbGci...` (Step 4 से) |
   | `CLOUDINARY_CLOUD_NAME` | `ict-daily-school` (Step 5 से) |
   | `CLOUDINARY_API_KEY` | `12345...` (Step 5 से) |
   | `CLOUDINARY_API_SECRET` | `abcDef...` (Step 5 से) |
   | `TRIGGER_API_KEY` | कोई भी strong password बनाएं, जैसे: `TrG@2024$ecureKey!` |
   | `TEACHER_NAME` | अपना नाम, जैसे: `श्री शर्मा जी` |
   | `SCHOOL_NAME` | अपने school का नाम |
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | कोई भी लंबा random text, जैसे: `xK9m$2pL@qR5nW8v` |

   > 💡 **`TRIGGER_API_KEY`** — यह वो password है जो GitHub Actions daily trigger के लिए use करेगा। कुछ भी strong password रखें और **याद रखें** — Step 8 में फिर चाहिए होगा!

   > ⚠️ **`APP_BASE_URL`** — यह अभी खाली छोड़ दें, deploy होने के बाद add करेंगे

**7.10)** **"Create Web Service"** पर click करें

**7.11)** ⏰ **Deploy शुरू हो जाएगा!** 
   - Build log दिखेगा (बहुत सारा text scroll होगा — normal है!)
   - **5-10 minutes** लग सकते हैं
   - Wait करें जब तक status **"Live"** 🟢 (green dot) न दिखे

**7.12)** Deploy complete होने पर:
   - ऊपर आपका app URL दिखेगा:
     ```
     https://ict-daily-agent.onrender.com
     ```
   - 📝 इसे copy करें!

**7.13)** अब **`APP_BASE_URL`** environment variable add करें:
   - Render Dashboard → अपना service → **"Environment"** tab
   - **"Add Environment Variable"** पर click करें:
     - Key: `APP_BASE_URL`
     - Value: `https://ict-daily-agent.onrender.com` (अभी copy किया हुआ URL)
   - **"Save Changes"** पर click करें
   - App automatically redeploy होगा (2-3 minutes)

### ✅ Verify:
- ✅ Render Dashboard पर status **"Live"** 🟢 दिख रहा है
- ✅ Browser में `https://ict-daily-agent.onrender.com/health` खोलने पर `{"status": "ok"}` दिखता है
- ✅ `https://ict-daily-agent.onrender.com/dashboard` खोलने पर dashboard page दिखता है

### ⚠️ Free Tier Note:
- Free tier पर app **15 minutes inactivity** के बाद "sleep" हो जाता है
- अगली request पर **30-60 seconds** लगते हैं wake up होने में
- यह normal है! Daily trigger के लिए GitHub Actions workflow में wake-up step पहले से है

---

## Step 8: ⚡ GitHub Actions Setup करें (Daily Auto-Run)

### 📌 GitHub Actions क्या है?
GitHub Actions एक free service है जो **automatically हर रोज़ सुबह 8 बजे** हमारे app को trigger करती है PDF बनाने के लिए। यह एक automatic alarm clock जैसा है!

### 📝 Step-by-Step:

**8.1)** GitHub पर अपने repository में जाएं:
   - `https://github.com/YOUR_USERNAME/ict-daily-agent`

**8.2)** **"Settings"** tab पर click करें (⚙️ gear icon, repository के tabs में)

**8.3)** बाएं menu में → **"Secrets and variables"** → **"Actions"** पर click करें

**8.4)** **"New repository secret"** button पर click करें

**8.5)** दो secrets add करें (एक-एक करके):

   **Secret 1:**
   - **Name:** `TRIGGER_API_KEY`
   - **Secret:** वही password जो आपने Step 7.9 में `TRIGGER_API_KEY` environment variable में डाला था
     - Example: `TrG@2024$ecureKey!`
   - **"Add secret"** पर click करें

   **Secret 2:**
   - **Name:** `RENDER_APP_URL`
   - **Secret:** आपका Render app URL
     - Example: `https://ict-daily-agent.onrender.com`
   - **"Add secret"** पर click करें

**8.6)** ✅ दोनों secrets added दिखने चाहिए:
   ```
   RENDER_APP_URL    Updated just now
   TRIGGER_API_KEY   Updated just now
   ```

---

### 📝 Part B: GitHub Actions Enable करें

**8.7)** Repository में **"Actions"** tab पर click करें (tabs में, ▶️ icon)

**8.8)** अगर "Get started with GitHub Actions" page दिखे:
   - **"I understand my workflows, go ahead and enable them"** पर click करें
   - या workflow suggestion ignore करें

**8.9)** बाएं sidebar में **"📄 Daily PDF Generation"** workflow दिखेगा — click करें

---

### 📝 Part C: Manual Test Run करें

**8.10)** **"Run workflow"** dropdown button पर click करें (दाईं तरफ)

**8.11)** Options दिखेंगे:
   - **Branch:** `main` (default, इसे न बदलें)
   - **Class/Standard:** खाली छोड़ दें (all classes)
   - **Force topic:** खाली छोड़ दें (auto-select)

**8.12)** **"Run workflow"** (green button) पर click करें

**8.13)** Page refresh करें (F5) — एक new workflow run दिखेगा

**8.14)** उस run पर click करें → status देखें:
   - 🟡 **In progress** — चल रहा है
   - 🟢 **Success** — सफलतापूर्वक हो गया ✅
   - 🔴 **Failed** — कोई error हुई (click करके details देखें)

**8.15)** अगर **Success** ✅ दिखे:
   - 🎉 बधाई! अब यह **हर रोज़ सुबह 8:00 AM IST** पर automatically चलेगा!
   - अपना WhatsApp check करें — PDF message आना चाहिए!

### ✅ Verify:
- ✅ दोनों secrets (TRIGGER_API_KEY, RENDER_APP_URL) add हो गए
- ✅ Actions tab में "📄 Daily PDF Generation" workflow दिख रहा है
- ✅ Manual test run **Success** ✅ हो गया

### 📅 Schedule:
- यह workflow **हर रोज़ सुबह 2:30 AM UTC = 8:00 AM IST** पर automatically चलेगा
- ⚠️ GitHub Actions में ±5-15 minutes की delay हो सकती है — यह normal है

---

## Step 9: 📱 WhatsApp पर Students को Setup करें

### 📌 WhatsApp API Rules:
WhatsApp Cloud API में एक important rule है: **Student को पहले आपके WhatsApp Business number पर message भेजना ज़रूरी है** (opt-in)। बिना opt-in के आप उन्हें message नहीं भेज सकते।

### 📝 Step-by-Step:

**9.1)** अपना **WhatsApp Business Number** note करें:
   - Meta Developer Console → WhatsApp → API Setup
   - "From" section में जो number दिखता है, वो आपका WhatsApp Business number है
   - 💡 Test number format: `+1 (555) 123-4567`

**9.2)** Students को instructions दें (class में या parents WhatsApp group में):

   > 📢 **Students/Parents से share करने का message:**
   > 
   > ```
   > 🎓 प्रिय छात्र/अभिभावक,
   > 
   > हम अब हर रोज़ WhatsApp पर study material (PDF) भेजेंगे।
   > इसके लिए कृपया नीचे दिए number पर "Hi" message भेजें:
   > 
   > 📱 Number: +1 555 123 4567
   > (या इस link पर click करें: https://wa.me/15551234567?text=Hi)
   > 
   > "Hi" भेजने के बाद आपको daily PDF मिलना शुरू हो जाएगा।
   > 
   > धन्यवाद! 🙏
   > - [आपका नाम], [School Name]
   > ```

**9.3)** जब student "Hi" भेजेगा:
   - आपका system automatically उसे registered कर लेगा
   - अगले दिन से उसे PDF मिलना शुरू हो जाएगा

**9.4)** Students की list **database** में add करें (Supabase):
   - Supabase Dashboard → Table Editor → `whatsapp_contacts` table
   - **"Insert"** → **"Insert Row"** पर click करें
   - Details भरें:
     - `student_name`: छात्र का नाम
     - `phone_number`: `919876543210` (91 + 10-digit number, बिना + के)
     - `class_standard`: `10` (या जो class हो)
     - `is_active`: `true`
   - **"Save"** पर click करें

**9.5)** सभी students को इसी तरह add करें

### 💡 Bulk Add करने का तरीका (एक साथ बहुत students):

Supabase SQL Editor में जाकर यह query run करें:
```sql
INSERT INTO whatsapp_contacts (student_name, phone_number, class_standard) VALUES
('राहुल शर्मा', '919876543210', '10'),
('प्रिया सिंह', '919876543211', '10'),
('अमित कुमार', '919876543212', '10'),
('नेहा गुप्ता', '919876543213', '10');
-- ↑ अपने students की details डालें
```

### ✅ Verify:
- ✅ Students ने WhatsApp Business number पर "Hi" भेजा
- ✅ `whatsapp_contacts` table में students की list दिख रही है
- ✅ `is_active` = `true` है सभी students के लिए

---

## Step 10: 🧪 Testing करें 🎉

### अब सब कुछ test करते हैं!

---

### 🧪 Test 1: Dashboard Check
**10.1)** Browser में खोलें: `https://ict-daily-agent.onrender.com/dashboard`
   - ⏰ अगर पहली बार खोल रहे हैं तो 30-60 seconds लग सकते हैं (free tier wake up)
   - Dashboard page दिखना चाहिए

### 🧪 Test 2: Health Check
**10.2)** Browser में खोलें: `https://ict-daily-agent.onrender.com/health`
   - Response आना चाहिए:
     ```json
     {"status": "ok"}
     ```

### 🧪 Test 3: Manual PDF Generation
**10.3)** GitHub → Actions tab → "📄 Daily PDF Generation" → "Run workflow" → "Run workflow"
   - Wait करें (5-10 minutes)
   - Status **green** ✅ होना चाहिए
   - WhatsApp पर PDF message आना चाहिए

### 🧪 Test 4: Response Form
**10.4)** WhatsApp पर आए message में feedback form का link होगा — click करें
   - Form भरें:
     - Name: अपना test name
     - Class: 10
     - Understanding: Easy
     - Quiz: कुछ भी भरें
   - Submit करें

### 🧪 Test 5: Dashboard Data Check
**10.5)** Dashboard फिर से refresh करें
   - अभी submit किया हुआ response दिखना चाहिए
   - Topic history में आज का topic दिखना चाहिए

### 🧪 Test 6: Database Check
**10.6)** Supabase Dashboard → Table Editor:
   - `topic_history` — आज का topic दिखना चाहिए
   - `student_responses` — आपका test response दिखना चाहिए

### ✅ अगर सभी 6 tests pass हो गए:
> 🎉🎉🎉 **बधाई हो! आपका ICT Daily PDF System पूरी तरह तैयार है!**
> 
> अब हर रोज़ सुबह 8 बजे automatically PDF बनकर students के WhatsApp पर पहुंच जाएगी!

---

## 🔧 समस्या समाधान (Troubleshooting)

### ❌ समस्या 1: Render.com पर deploy fail हो रहा है

**लक्षण:** Build log में red error दिख रहा है

**समाधान:**
1. Render Dashboard → अपना service → **"Logs"** tab पर click करें
2. Error message पढ़ें:
   - `ModuleNotFoundError: No module named 'xxx'` → `requirements.txt` में वो module add करें
   - `Error: Could not find a version...` → Python version issue, `runtime.txt` check करें
3. **"Manual Deploy"** → **"Deploy latest commit"** पर click करें

---

### ❌ समस्या 2: WhatsApp message नहीं आ रहा

**लक्षण:** PDF बनता है लेकिन WhatsApp पर नहीं आता

**समाधान:**
1. ✅ Check करें: क्या student ने पहले "Hi" भेजा है? (24-hour window rule)
2. ✅ Check करें: `WHATSAPP_TOKEN` सही है? (Permanent token use करें, temporary नहीं)
3. ✅ Check करें: `WHATSAPP_PHONE_NUMBER_ID` सही है?
4. ✅ Check करें: Message template **Approved** है?
5. Meta Developer Console → WhatsApp → **"Insights"** में errors देखें
6. Render Dashboard → **"Logs"** में WhatsApp related errors ढूंढें

---

### ❌ समस्या 3: GitHub Actions fail हो रहा है

**लक्षण:** Actions tab में workflow run **red** ❌ दिख रहा है

**समाधान:**
1. Failed run पर click करें → error details पढ़ें
2. Common errors:
   - `TRIGGER_API_KEY secret is not set` → Step 8.5 फिर से करें
   - `RENDER_APP_URL secret is not set` → Step 8.5 फिर से करें
   - `HTTP 401` → TRIGGER_API_KEY Render पर और GitHub secret में same होनी चाहिए
   - `HTTP 500` → App में error है, Render logs check करें
   - `Connection timeout` → Render free tier wake up time, दोबारा try करें

---

### ❌ समस्या 4: Dashboard नहीं खुल रहा / बहुत slow है

**लक्षण:** "Loading..." बहुत देर दिखता है या error page आता है

**समाधान:**
1. **Free tier wake up:** पहली request पर 30-60 sec लगते हैं — normal है
2. ✅ URL सही है? (`https://ict-daily-agent.onrender.com/dashboard`)
3. Render Dashboard → check करें service **"Live"** 🟢 है
4. अगर service **"Suspended"** है → free tier limit पूरी हो गई, next month शुरू होने का wait करें

---

### ❌ समस्या 5: Gemini API error

**लक्षण:** PDF content खाली है या error दिखता है

**समाधान:**
1. ✅ `GEMINI_API_KEY` सही है? (Google AI Studio से verify करें)
2. ✅ Free tier quota पूरा तो नहीं हो गया? (AI Studio → API Keys → Usage देखें)
3. Google AI Studio पर जाकर manually test करें — अगर वहां काम करे तो key सही है

---

### ❌ समस्या 6: Supabase error / Data save नहीं हो रहा

**लक्षण:** Responses save नहीं हो रहे, dashboard खाली दिखता है

**समाधान:**
1. ✅ `SUPABASE_URL` और `SUPABASE_KEY` सही हैं?
2. Supabase Dashboard → Table Editor → check करें tables exist करते हैं
3. अगर tables नहीं हैं → Step 4.10 का SQL code फिर से run करें
4. Supabase Dashboard → **"Logs"** → API logs check करें

---

### ❌ समस्या 7: Temporary WhatsApp Token expire हो गया

**लक्षण:** "Error 401: OAuthException" WhatsApp API से

**समाधान:**
- 🔴 आपने temporary token use किया है! Step 3 Part E follow करके **permanent token** बनाएं
- Permanent token बनाने के बाद:
  1. Render Dashboard → Environment → `WHATSAPP_TOKEN` update करें
  2. App automatically redeploy होगा

---

## 💰 Free Tier Limits — क्या जानना ज़रूरी है

| Service | Free Limit | 40 Students Daily Use | Safe? |
|---------|-----------|----------------------|-------|
| **Render.com** | 750 hours/month | 24/7 = 720 hours | ✅ Safe |
| **WhatsApp** | 1,000 conversations/month | ~40/day × 30 = 1,200 | ⚠️ Close |
| **Gemini AI** | 60 requests/min, 1,500/day | ~5-10/day | ✅ Very Safe |
| **Supabase** | 500 MB database | ~50KB/day | ✅ Very Safe |
| **Cloudinary** | 25 GB storage | ~2MB/day PDF | ✅ Very Safe |
| **GitHub Actions** | 2,000 min/month | ~5 min/day = 150 min | ✅ Safe |

### ⚠️ WhatsApp Free Limit Tips:
- Free tier: **1,000 service-initiated conversations/month**
- 40 students × 30 days = 1,200 — यह limit के करीब है
- **Solutions:**
  - कम students (30-35) को daily भेजें
  - कुछ दिन skip करें (weekends, holidays)
  - या Meta Business verification करके limit बढ़ाएं (free)

### 💡 Render.com Free Tier:
- App **15 min** inactivity के बाद sleep हो जाता है
- Next request पर **30-60 sec** wake up time लगता है
- Monthly 750 hours free — 1 app 24/7 चलाने के लिए काफी
- ⚠️ अगर app sleep से wake up नहीं हो रहा → Render Dashboard check करें

---

## 📞 मदद चाहिए?

### 🔍 Logs कैसे देखें (Debugging):

**Render.com Logs:**
1. https://dashboard.render.com पर जाएं
2. अपना `ict-daily-agent` service पर click करें
3. **"Logs"** tab पर click करें
4. Real-time logs दिखेंगे — errors यहाँ ढूंढें

**GitHub Actions Logs:**
1. GitHub repo → **Actions** tab
2. Latest run पर click करें
3. Job name पर click करें
4. Step-by-step logs दिखेंगे

**Supabase Logs:**
1. Supabase Dashboard → **"Logs"** (बाएं menu)
2. **"API Logs"** → database request logs

---

### 📋 Notepad File (my-api-keys.txt) — यह कैसी दिखनी चाहिए:

```
═══════════════════════════════════════════
  ICT Daily Agent — My API Keys
  ⚠️ किसी को न दिखाएं!
═══════════════════════════════════════════

📱 WHATSAPP:
  WHATSAPP_TOKEN = EAAxxxxxxxxxxxxx (PERMANENT)
  WHATSAPP_PHONE_NUMBER_ID = 1234567890123456

🤖 GEMINI AI:
  GEMINI_API_KEY = AIzaSyD_xxxxxxxxxxxx

🗄️ SUPABASE:
  SUPABASE_URL = https://xxxxxxxxxxxx.supabase.co
  SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

🌤️ CLOUDINARY:
  CLOUDINARY_CLOUD_NAME = ict-daily-school
  CLOUDINARY_API_KEY = 123456789012345
  CLOUDINARY_API_SECRET = abcDefGHijklMNOpqrSTUvwxyz

🚀 RENDER:
  APP URL = https://ict-daily-agent.onrender.com

🔐 OTHER:
  TRIGGER_API_KEY = TrG@2024$ecureKey!
  SECRET_KEY = xK9m$2pL@qR5nW8v
  WHATSAPP_VERIFY_TOKEN = my_school_verify_2024

═══════════════════════════════════════════
```

---

### 🔄 Important Daily/Weekly Tasks:

| Task | कब करें | कैसे करें |
|------|---------|-----------|
| Dashboard check | रोज़ शाम | Browser में dashboard URL खोलें |
| Student responses देखें | रोज़ शाम | Dashboard → Responses section |
| Render logs check | Weekly | Render Dashboard → Logs |
| WhatsApp usage check | Monthly | Meta Developer Console → Insights |
| Supabase storage check | Monthly | Supabase Dashboard → Usage |

---

### 🎓 बधाई! 🎉

आपने successfully ICT Daily PDF Agent setup कर लिया है!

अब हर रोज़ सुबह 8 बजे:
1. 🤖 AI automatically एक नया topic चुनेगा
2. 📄 एक सुंदर PDF बनेगी
3. 📱 WhatsApp पर students को भेजी जाएगी
4. 📊 शाम को आप dashboard पर responses देखेंगे

> **"Technology should work for the teacher, not the other way around."** 🙏

---

*यह guide ICT Daily PDF Agent project का हिस्सा है।*
*Last Updated: May 2026*
