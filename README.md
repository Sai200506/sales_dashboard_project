# Sales Data Dashboard

A comprehensive web application built with Python Flask for uploading sales data and generating meaningful insights through interactive dashboards and visualizations.

## Features

- 📊 **Interactive Dashboard**: Beautiful, responsive dashboard with key metrics and visualizations
- 📁 **File Upload**: Support for CSV and Excel files (.csv, .xlsx, .xls)
- 📈 **Automatic Insights**: Intelligent column detection and automatic generation of:
  - Sales timeline analysis
  - Sales amount distribution
  - Top products by revenue
  - Summary statistics
  - Data preview and overview
- 🎨 **Modern UI**: Bootstrap-powered responsive design with custom styling
- 📱 **Mobile Friendly**: Fully responsive design that works on all devices

## Technology Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone/Download the project**
   ```bash
   # If you have this as a git repository
   git clone <repository-url>
   cd sales_dashboard_project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Upload your sales data and explore the dashboard!

## Usage

### Data Format Requirements

Your sales data should include columns with names containing:
- **Date columns**: date, time, created, order
- **Amount columns**: amount, price, total, revenue, sales, value
- **Product columns**: product, item, name, category
- **Customer columns**: customer, client, user, buyer

### Example Data Format

```csv
Date,Product,Customer,Amount,Category,Region
2024-01-15,Laptop Dell XPS,John Smith,1299.99,Electronics,North
2024-01-16,iPhone 15,Sarah Johnson,999.00,Electronics,South
```

### Sample Data

Use the included `sample_sales_data.csv` file to test the application.

## Project Structure

```
sales_dashboard_project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_sales_data.csv  # Sample data for testing
├── templates/             # HTML templates
│   ├── upload.html       # File upload page
│   └── dashboard.html    # Dashboard display page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   └── js/              # JavaScript files (for future enhancements)
└── uploads/             # Directory for uploaded files
```

## Features Explanation

### Automatic Column Detection
The system intelligently identifies different types of columns based on common naming patterns:
- Automatically detects date, amount, product, and customer columns
- Generates appropriate visualizations based on available data

### Generated Insights
- **Key Metrics**: Total sales, average sale amount, maximum sale, record count
- **Time Series Analysis**: Sales trends over time
- **Distribution Analysis**: Sales amount distribution histogram
- **Top Performers**: Top 10 products by sales revenue
- **Statistical Summary**: Descriptive statistics for all numeric columns

### Security Features
- File type validation (only CSV and Excel files allowed)
- Secure filename handling
- File size limits (16MB maximum)
- Timestamp-based file naming to prevent conflicts

## Customization

### Adding New Visualizations
To add new charts, modify the `process_sales_data()` function in `app.py`:

```python
# Example: Add a new chart
if category_cols and amount_cols:
    category_sales = df.groupby(category_cols[0])[amount_cols[0]].sum()
    fig = go.Figure(data=[go.Pie(labels=category_sales.index, values=category_sales.values)])
    insights['charts']['category_pie'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
```

### Styling Customization
Edit `static/css/style.css` to customize the appearance of the dashboard.

## Troubleshooting

### Common Issues

1. **Module not found errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct Python environment

2. **File upload errors**
   - Verify file format is CSV or Excel
   - Check that file size is under 16MB
   - Ensure file has proper column headers

3. **No charts displayed**
   - Verify your data has recognizable column names
   - Check browser console for JavaScript errors
   - Ensure Plotly library is loading correctly

## Future Enhancements

- [ ] Database integration for persistent data storage
- [ ] User authentication and multi-user support
- [ ] More advanced analytics (forecasting, trends)
- [ ] Export functionality for reports
- [ ] Real-time data updates
- [ ] Custom column mapping interface
- [ ] Advanced filtering and drill-down capabilities

## Contributing

This is a college project template. Feel free to:
- Add new visualization types
- Improve the UI/UX
- Add more data processing features
- Enhance error handling
- Add tests

## License

This project is for educational purposes.

## Contact

For questions about this project, please refer to your course materials or instructor.
