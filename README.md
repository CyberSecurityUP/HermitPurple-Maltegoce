**HermitPurple: A Comprehensive Data Extraction and Analysis Transform for Maltego**

**Overview**

HermitPurple is an advanced Transform designed for Maltego, focusing on robust data extraction and analysis capabilities across various digital environments, including the Tor network, surface web, and specialized search platforms like Ahmia. This tool is especially valuable for cybersecurity professionals, digital forensic investigators, and researchers who need to delve into both the surface and dark web to gather intelligence and conduct thorough digital investigations.

**Features**
- **Multi-Source Data Extraction**: Seamlessly extracts data from the Tor network, surface web, and the Ahmia search engine, ensuring a comprehensive coverage across different layers of the internet.
- **Person Finder**: Incorporates a specialized module for searching missing individuals by interfacing with global missing person databases.
- **Unique Domain Extraction**: From Ahmia search results, it filters and presents each domain uniquely to avoid duplication and streamline the analysis process.
- **Dynamic Operational Feedback**: Provides dynamic responses within Maltego, including notifications when no results are found, enhancing user interaction and efficiency.

**How It Works**
HermitPurple operates by performing targeted searches across selected platforms based on user-defined criteria. For the Tor network, it routes requests through Tor proxies to access .onion sites securely. On the surface web, it employs sophisticated scraping techniques to gather actionable data. In searches for missing people, it accesses and queries global databases, presenting found data neatly within Maltego’s interactive interface.

**Use Cases**
- **Cybersecurity Monitoring**: Track and analyze domains associated with malicious dark web activities or data breaches.
- **Academic Studies**: Facilitate research into the scale and scope of content across different internet layers.
- **Missing Persons Investigations**: Aid law enforcement and investigators in tracing and locating missing individuals through digital footprints.

**Setup**
1. Clone the HermitPurple repository.
2. Install all required dependencies.
3. Configure the Transform within Maltego, setting the appropriate script paths and input types.
4. Initiate the Transform from a Phrase entity or directly input relevant search terms.

**Dependencies**
- **Python 3.x**
- **Essential Libraries**: requests, beautifulsoup4, lxml, socksipy for handling Tor connections.

**Author**
- **Joas A Santos**

HermitPurple is part of an extensive toolkit aimed at enhancing digital investigative capabilities within the Maltego framework. It provides investigators with the necessary tools to perform in-depth analysis of online data, offering insights that are crucial for both preventative cybersecurity measures and active investigations.

--

![image](https://github.com/CyberSecurityUP/HermitPurple-Maltegoce/assets/34966120/d0a3fdbc-6f85-4669-9fe2-c924a81223e7)
