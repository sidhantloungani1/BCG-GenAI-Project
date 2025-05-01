import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

df = pd.read_csv('bcgx data.csv')

@app.route('/', methods=['GET', 'POST'])

def chat():
    response=""
    user_query=""

    if request.method == 'POST':
        user_query = request.form['query'].lower()
        
        if 'average profit margin' in user_query:
            company = extract_company(user_query)
            df["profit_margin"] = df['Net Income'] / df['Total Revenue']
            if company:
                avg_pm = df[df['Company'].str.lower() == company]['profit_margin'].mean()
                response = f"Average profit margin for {company.title()} is {avg_pm:.2%}"
            else:
                response = "Please specify company name"
        elif "revenue trend" in user_query:
            company = extract_company(user_query)
            if company:
                trend = df[df['Company'].str.lower() == company][['Year', 'Total Revenue']].sort_values('Year')
                response = f"Revenue trend for {company.title()}:<br>"
                for _, row in trend.iterrows():
                    response += f"{row['Year']}: {int(row['Total Revenue'])}<br>"
            else:
                response = "Please specify a company."

        elif "debt to asset" in user_query:
            company = extract_company(user_query)
            df['Debt to Asset Ratio'] = df['Total Liabilities'] / df['Total Assets']
            if company:
                avg_ratio = df[df['Company'].str.lower() == company]['Debt to Asset Ratio'].mean()
                response = f"Average debt-to-asset ratio for {company.title()} is {avg_ratio:.2%}"
            else:
                response = "Please specify a company."

        else:
            response = "Sorry, I couldn't understand your query. Try asking about profit margin, revenue trend, or debt to asset ratio."

    return render_template('chat.html', user_query=user_query, response=response)

def extract_company(query):
    companies=['tesla', 'apple', 'microsoft']
    for company in companies:
        if company in query:
            return company
    return None
    
if __name__ == '__main__':
    app.run(debug=True)