# Discounted Cash Flow (DCF) Valuation Model

Welcome to the DCF Valuation Model repository. This project is designed to perform comprehensive financial forecasting and valuation using the Discounted Cash Flow methodology.

## Youtube Explanation
[![Discounted Cash Flow (DCF) calculations with monte-carlo simulations in python | Stock Analysis](https://img.youtube.com/vi/Qt-FsYG-IGI/0.jpg)](https://www.youtube.com/watch?v=Qt-FsYG-IGI&autoplay=1)

## Try it here 
[Streamlit]([www.google.com](https://dcf-valuation-model.streamlit.app/))


## Workflow
```mermaid
flowchart TB
    %% Styles
    classDef input fill:#000099,stroke:#333,stroke-width:2px
    classDef processing fill:#913f7a,stroke:#333,stroke-width:2px
    classDef analysis fill:#88a000,stroke:#333,stroke-width:2px
    classDef output fill:#be4d25,stroke:#333,stroke-width:2px
    classDef storage fill:#640bbf,stroke:#333,stroke-width:2px
    
    %% Input Layer
    subgraph Input
        UI[Input Interface]:::input
        DataHandler[Data Handler]:::input
        DB[(Historical Data)]:::storage
    end
    
    %% Processing Layer
    subgraph Processing
        DataProc[Data Processing Module]:::processing
        Forecast[Forecasting Engine]:::processing
        Monte[Monte Carlo Engine]:::analysis
        DCF[DCF Calculation Core]:::analysis
    end
    
    %% Output Layer
    subgraph Output
        Report[Report Generator]:::output
        Visual[Visualization]:::output
        Export[Export Formats]:::output
    end
    
    %% Connections
    UI --> DataHandler
    DataHandler --> DB
    DB --> DataProc
    DataProc --> Forecast
    Forecast <--> Monte
    Monte --> DCF
    DCF --> Report
    Report --> Visual
    Report --> Export

```

## Directory Structure
```
arnavagarwal-mr-ar-dcf_valuation_model/
├── app.py                # Main application file to integrate the modules
├── data_processing.py    # Module for cleaning and preparing financial data
├── dcf_calculation.py    # Core logic for DCF calculations
├── forecasting.py        # Financial forecasting logic
├── monte.py              # Monte Carlo simulations for sensitivity analysis
└── report_generator.py   # Generate reports based on DCF analysis
```



## Features
- **Data Preprocessing**: Clean and prepare financial data.
- **DCF Calculation**: Perform accurate valuations using Free Cash Flow projections.
- **Forecasting**: Generate future projections using historical trends and user assumptions.
- **Monte Carlo Simulation**: Analyze risks and sensitivities.
- **Report Generation**: Create professional reports for stakeholders.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature/my-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a Pull Request.

## Contact me 📪
<div id="badges">
  <a href="https://www.linkedin.com/in/arnav-agarwal-571a59243/" target="blank">
   <img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
 <a href="https://www.instagram.com/arnav_executes?igsh=MWUxaWlkanZob2lqeA==" target="blank">
 <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"  alt="Instagram Badge" />
 </a>
 </a>
 <a href="https://medium.com/@arumynameis" target="blank">
 <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white"  alt="Medium Badge" />
 </a>
</div>


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
Special thanks to all contributors and the financial modeling community for their support and guidance.
