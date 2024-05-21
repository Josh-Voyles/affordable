# **Home-Choice-Pro**

## **Overview**
Many home buyers use a calculator to determine their monthly house payment, but they are often surprised by additional, unexpected payments that come with home ownership. This project aims to create a comprehensive mortgage calculator application that will benefit potential home buyers and realtors by helping them determine the price of a house that is realistically within their budget.

## **Installation & Contributing**
1. Reference [CONTRIBUTING.md](https://github.com/Josh-Voyles/Home-Choice-Pro/blob/readme/CONTRIBUTING.md) for instructions. 

### **Key Features**
-  Monthly Budget Calculation: Determine the maximum house price based on the user's monthly budget.
-  Comprehensive Expense Calculation: Calculate monthly expenses including principal, interest, property taxes, and insurance.
-  Hidden Costs: Factor in hidden costs such as ongoing maintenance, potential repairs, homeowners’ association fees, etc.
-  User-Friendly Interface: Desktop GUI designed for ease of use by consumers and realtors.
-  Additional Analysis: Potential features to analyze the long-term financial impact of renting versus buying and to calculate mortgage with direct input.


### **Benefits**
-  Accurate Budget Estimation: Helps users get an accurate estimate of the price range of homes they can afford.
-  Transparent Cost Breakdown: Provides transparency on all possible costs associated with home ownership.
-  Informed Decision-Making: Empowers users with detailed financial insights to make informed home-buying decisions.

## **File Structure**
```
Home-Choice-Pro/
│
├── main.py                # Entry point of the application
├── requirements.txt       # List of project dependencies
├── README.md              # Project overview and documentation
├── LICENSE                # License information
│
├── app/                   # Main application package
│   ├── __init__.py
│   ├── main_window.py     # Main window class
│   ├── controllers/       # Controllers for handling logic & analytics
│   ├── models/            # Data models (for analytics and logic classes)
│   └── views/             # UI files and components
│       ├── __init__.py
│       ├── main_window.ui # UI file created with Qt Designer
│       └── other_ui.ui    # Other UI files
│
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_main.py
│   └── other_tests.py
│
└── resources/             # Resources like images, icons, etc.
    ├── images/
    ├── icons/
    └── styles/
```

## **Contributors:**
- Randy Shreeves
- Josh Voyles
- Joey Garcia
- Zaria Gibbs

## LICENSE
This project is licensed under the GPL-3.0 license - see the LICENSE file for details.
