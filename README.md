# **BI Assistant: The Manager's Ultimate Data Solution**🚀

The **BI Assistant** is a comprehensive and intelligent solution designed to empower company managers by providing seamless data management, insightful analysis, and interactive communication through an AI-driven chatbot. Combining cutting-edge technologies like **ETL pipelines**, a **data warehouse**, **Power BI dashboards**, and a **Streamlit-powered chatbot**, this project delivers an end-to-end business intelligence (BI) framework for making informed, data-driven decisions.

---

## **Key Features and Components**🚀

### **1. Automated ETL Pipelines**
- Fully automated **Extract, Transform, Load (ETL)** processes to ensure data is always clean, accurate, and up-to-date Using **SSIS**.  
- Handles diverse data sources and transforms raw data into a structured format ready for advanced analysis.  
- SQL scripts provided in the `/sql-scripts` folder offer complete transparency and flexibility for customization.  

---

### **2. Robust Data Warehouse**
- A high-performance, centralized repository designed for efficient querying and data analysis.  
- Stores clean, pre-processed datasets, optimized for powering the chatbot and visual dashboards.  
- Enables scalable storage and rapid access to actionable insights.  

---

### **3. Advanced Power BI Dashboards**
- Professional-grade visualizations to unlock trends, analyze employee performance, and reveal critical business insights.  
- Fully interactive and customizable, giving managers the power to drill down into specific data points or zoom out to view the bigger picture.  
- Helps decision-makers easily monitor KPIs, track progress, and identify opportunities for growth.

---

### **4. Intelligent Streamlit-Powered Chatbot**

- **AI-Driven Query Resolution**: Built with **LangChain** and powered by **Gemini**, this chatbot allows managers to ask questions in natural language and receive precise, data-backed responses.
  
- **chatbot** integrated with the DW to answer managers' queries dynamically.
  
- **Multilingual Support**: Managers can ask questions in **Arabic or English**, making it accessible for a wider range of users.

- **Serious or Non-Serious Queries**:  
  - The chatbot can handle both **serious queries** related to the **data warehouse**, such as performance trends, revenue analysis, or employee statistics.  
  - It also accommodates **non-serious queries**, such as casual conversations, jokes, or general knowledge, to ensure a more engaging user experience.

- **Actionable Insights**: Goes beyond answering queries to provide proactive recommendations for improvement based on analyzed trends and patterns.

- **Seamless Interaction**: A user-friendly interface powered by Streamlit ensures effortless communication and quick access to key insights without requiring technical expertise.


![alt text](<WhatsApp Image 2024-11-25 at 15.52.53_8e62a23e.jpg>)

---
## **Technologies Used**🚀
- **Data Warehousing**: SQL Server Integration Services (SSIS), SQL Server
- **Data Visualization**: Power BI
- **Chatbot Development**: Python, LLMs
- **Backend**: Streamlit
- **Database**: SQL Server, MySQL, Data Warehouse

## **How to Get Started**🚀

Follow these steps to set up and run the BI Assistant project:

### **Step 1: Clone the Repository**
To get started with the BI Assistant, clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-username/BI-Assistant.git
cd BI-Assistant
```

### **Step 2: Install Dependencies**
Ensure that all required Python libraries are installed by running the following command:

```bash
pip install -r requirements.txt

```
- Note: Make sure you have Python 3.10 or above installed on your system.



### **Step 3: Set Up the Data Warehouse**
1. Import the provided SQL scripts from the /sql-scripts folder into your database management system (e.g., MySQL, SSMS).
2. you might need to convert this script to Mysql Script to be run on MYSQL management.
3. Configure the connection details (host, port, user, password) in the project's configuration file (config.yaml).

### **Step 4: Set Up Gemini API Keys**

To integrate the chatbot with **Gemini**, you need to set up six API keys in a `.env` file. Follow these steps:

#### **1. Create a `.env` File**
- In the project root directory, create a `.env` file.  
#### **2. Add Your Gemini API Keys**
- Open the .env file in any text editor and add the following:
GEMINI_API_KEY_1=your_first_api_key
GEMINI_API_KEY_2=your_second_api_key
GEMINI_API_KEY_3=your_third_api_key
GEMINI_API_KEY_4=your_fourth_api_key
GEMINI_API_KEY_5=your_fifth_api_key
GEMINI_API_KEY_6=your_sixth_api_key
- Replace your_first_api_key, your_second_api_key, etc., with your actual API keys from Gemini.

### **Step 5: Launch the Streamlit Chatbot**
Start the chatbot interface to interact with your data:

```bash
streamlit run app.py
```

**Open the URL displayed in the terminal to access the chatbot in your browser.**

### **Step 6: View Power BI Dashboards**
- Open the Power BI file (dashboards/BI-Dashboard.pbix) using **Microsoft Power BI Desktop**.

## **Installation and Setup**
**Prerequisites**
- SQL Server with SSIS installed
- MySQL Workbench
- Python 3.10
- Required Python libraries (listed in requirements.txt)
- Power BI Desktop

## **Contributing**🚀

Contributions are welcome! If you'd like to contribute, follow these steps:  

1. **Fork this repository.**  
2. Create a new branch for your feature or fix:  
   ```bash
   git checkout -b feature-name
3. Commit your changes:
    ```bash
    git commit -m "Add new feature"
4. Push to the branch:
    ```bash
    git push origin feature-name
5. Submit a pull request.

## **Contact**😊

For further inquiries or support, feel free to reach out:

- **Email**: [mailto:gehan2065@outlook.com]
- **GitHub**: [https://github.com/gihankhalil1]
- **LinkedIn**: [https://www.linkedin.com/in/jihan-khalil-1b39a321a ]
