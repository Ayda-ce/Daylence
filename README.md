# Daylence - Daily Activities Planner

**Daylence** comes from **Day + Balance** - a small desktop app designed to help you build a balanced, realistic daily plan.

It lets you enter tasks with or without breaks, automatically adds appropriate rest periods, checks whether everything fits into 24 hours, and exports a clean Excel plan in both Persian and English.

---

## ✨ What the App Does (overall)

- Desktop GUI application built with **PyQt5** for daily planning 
- Three task lists:  
  - Activities **with breaks**  
  - Activities **without breaks**  
  - **Daily joint** activities  
- Smart rest-time calculation based on duration
- Detailed calculation page with breakdowns
- Excel export in **FA/EN** with styled tables
- Customizable **theme**, **font set**, and **row numbering style**
- Local-only: no accounts, no servers, no tracking
- Some parts of the application can be seen in the screenshots here:  
👉 **[View Screenshots](https://github.com/Ayda-ce/Daylence/tree/main/imgs)**


---

## 🚀 How It Works (Step by Step)

### 1. Launch & Splash Screen

- When you start Daylence, a **splash screen** appears first.
- The splash includes:
  - A short **sound**
  - An image based on the selected theme. 

---

### 2. Main Window - Adding Your Tasks

The main page includes **three tables**:

1. **Activities with breaks**
2. **Activities without breaks**
3. **Daily joint activities**

For each table:

- The first column is **Activity Name**
- The second column is **Duration** (`H:MM` format, e.g. `0:30`, `1:15`, `2:00`)

You can:

- Click in the first cell and start typing an activity name.
- Press **Tab** to move to the duration cell and type the time.
- Add as many rows as you want - there is no hard limit.
- Close and reopen the app and your last data will be loaded again (saved locally).

---

### 3. Using the Activity List (Predefined Activities)

Daylence includes a dialog with **predefined activity names** used for **autocomplete** When you start typing in the Activity Name cell on the main page,
  a dropdown appears suggesting items from this saved list.

- Click **“Show Activities”**.
- A dialog opens with a searchable table of activity names.
- You can:
  - Scroll through the predefined list
  - Edit existing items
  - Add new activities at the end
  - Save your changes with **OK**

There is no strict limit on the number of activities you can keep in this list.

---

### 4. Calculating the Schedule

Once you have filled activity names and times:

1. Click the **“Calculate”** button on the main window.
2. Daylence validates the times and opens the **Calculation Page**.

On the Calculation Page you’ll see three sections:

1. **Initial Activity Times**  
   - Shows your original activities and their durations.

2. **Activity Times** (with rest)  
   - For each activity, the app:
     - Splits very long tasks into smaller blocks if needed.
     - Inserts rest periods based on total duration.
     - Shows a detailed “Subduration” list (work + breaks) and the final total.

3. **Daily Schedule Times** (summary)  
   - Total time **with rest**
   - Total time **without rest**
   - Combined total time
   - Remaining time up to 24 hours
   - A **Status** field (Yes / No) telling you whether your plan fits in a single day

In this page you can either:

- Press **OK** to close the window  
- Press **Export Excel** to generate two Excel files

---

### 5. Exporting to Excel (FA / EN)
In calculation page click on **“Export Excel”** to create Excel output:

- The app asks you to choose a folder.
- It then generates **two Excel files**:
  - `plan_<date>_Fa.xlsx` (Persian)
  - `plan_<date>_En.xlsx` (English)

Each Excel file contains:

- A table of activities with estimated time
- A table for **physical** and **mental** state (starting at 10)
- The current date (Jalali or Gregorian)
- A **highlighted Sleep row**
- Styled headers, borders, and alternating row colors

These files are normal `.xlsx` files and can be opened in Excel, LibreOffice, etc.

---

### 6. About & Settings

At the bottom of the main window there are two links:

#### 🔹 About

- Opens a small dialog describing:
  - App name (**Daylence - Activities Planner**)
  - Current version
  - A short description of what the app does
  - Contact email for feedback

#### 🔹 Settings

- Opens the **Settings** dialog where you can customize:

1. **Theme**  
   - Choose from multiple color themes (e.g. `dark_red`, `dark_green`, `light`, `optimal_theme`, etc.)

2. **Font**  
   - Select from predefined font sets for the whole UI (titles, tables, buttons, etc.)

3. **Number Display**  
   - Choose how row numbers are shown in tables:
     - **Numbers**
     - **Roman numerals**
     - **Alphabetic** (a, b, c, …)

Your settings are saved locally and applied automatically next time you open Daylence.

---

## 🧩 Feature Summary

- Smart calculation of work + rest times  
- Splitting long tasks into smaller blocks  
- Full daily summary (with/without rest, remaining time, status)   
- Autocomplete for activity names  
- Multiple themes and font sets   
- Bilingual Excel export (FA/EN)  
- Splash screen with sound and theme-based image  
- All data stored locally on your device  

---

## 📥 Installation & Running Daylence

### Option 1 – Install the Ready-to-Use Version (Recommended)

1. Download the latest version from  [Releases](https://github.com/Ayda-ce/Daylence/releases/download/v1.0.15/Daylence_Setup.exe) 
2. Run the installer.
3. (Optional) Allow installation of the bundled Python runtime if prompted.
4. Launch **Daylence** from the Start Menu or the desktop shortcut.

---

### Option 2 - Run from Source (Developers)

> It is recommended to create and activate a **virtual environment** before running the following commands.

```bash
git clone https://github.com/Ayda-ce/Daylence.git
cd Daylence
pip install -r requirements.txt
cd src
python main.py
```
### Build the Executable Yourself (PyInstaller)

If you prefer to generate the executable manually from the source code, you can build it using PyInstaller.
Make sure dependencies are installed first:
```bash
pip install -r requirements.txt
```
Use the following command to build the EXE:
```bash
pyinstaller --noconfirm --windowed --onedir --clean --name "Daylence" --add-data "Files;Files" --hidden-import pandas --hidden-import openpyxl .\main.py
```
PowerShell multiline format:
```bash
pyinstaller `
  --noconfirm `
  --windowed `
  --onedir `
  --clean `
  --name "Daylence" `
  --add-data "Files;Files" `
  --hidden-import pandas `
  --hidden-import openpyxl `
  .\main.py
```
After the build completes, the executable will be located in:
```bash
dist/Daylence/
```
Run Daylence.exe inside that folder.
## 📬 Contact

For feedback, suggestions, or bug reports, feel free to reach out:

**Email:** daylence2025@gmail.com


## ⭐ Support

If you enjoy using Daylence or find it helpful, please consider giving the project a ⭐ star on GitHub.  
Your support helps the project grow!

## 🤝 Contribute
Contributions are welcome!  
Feel free to fork or clone the project. Each accepted contribution will be credited in the **Contributors** section.
