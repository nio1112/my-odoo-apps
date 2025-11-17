# My Odoo Apps - Ask Management System

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-green.svg)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org)

An enterprise-grade Ask Management System based on **Odoo 19.0**, designed for manufacturing and distribution businesses to optimize customer demand collection, inventory reservation, and procurement processes.

## 📋 Features Overview

### Core Features

#### 🛒 Ask Management (Ask Management)

- **Ask Order Management**: Support one-time and periodic (every 7/14/21/28 days) ask order creation
- **Multi-Channel Support**: Phone, email, customer portal, and manual input
- **Smart Workflow**: Draft → Submitted → Locked → Aggregated → Closed
- **Product Details**: Support multiple products and warehouses per ask order

#### 📦 Inventory Reservation System

- **Smart Reservation**: Create product reservations based on ask orders
- **Sales Binding**: Reservations can be bound to specific salespersons to ensure stock allocation
- **Validity Management**: 14-day default reservation validity with expiry reminders
- **Delivery Control**: Only the designated salesperson can validate delivery of reserved products

#### 📊 Procurement Decision Support

- **Data Aggregation**: Automatically aggregates demand from all locked ask orders
- **Procurement Dashboard**: Suggests purchase quantities by product and warehouse
- **Historical Analysis**: Calculates recommended purchase quantities based on historical data
- **Vendor Coordination**: Supports linking and tracking purchase orders

#### ⏰ Automated Scheduling

- **Daily Cutoff**: Automatically locks ask orders and demand at 23:59 every day
- **State Transition**: Automatically copies requested quantity to confirmed quantity on lock
- **Audit Log**: Full history of status changes and quantity adjustments
- **Storage Fees**: Automatically calculates storage cost for overdue reservations

## 🏗️ System Architecture

```text
my-odoo-apps/
├── addons/
│   └── odoo_ask/                 # Ask Management module
│       ├── models/               # Data models
│       │   ├── ask.py            # Core Ask model
│       │   ├── reservation.py    # Reservation model
│       │   ├── stock_picking.py  # Stock picking extension
│       │   └── scheduler.py      # Scheduled jobs
│       ├── wizard/               # Wizards
│       │   └── ask_wizard.py     # Ask creation wizard
│       ├── views/                # View definitions
│       │   ├── ask_views.xml                 # Ask form/list views
│       │   ├── reservation_views.xml        # Reservation views
│       │   └── procurement_dashboard.xml    # Procurement dashboard
│       ├── security/            # Access control
│       ├── data/                # Initial data
│       └── static/              # Static assets
├── docker-compose.yml           # Docker deployment
└── README.md                    # Project documentation
```

## 🚀 Getting Started

### Requirements

- Docker 20.10+
- Docker Compose 2.0+
- At least 4GB available RAM

### One-Click Deployment

```bash
# Clone the project
git clone https://github.com/nio1112/my-odoo-apps.git
cd my-odoo-apps

# Start services
docker-compose up -d

# Wait for Odoo to start (about 1–2 minutes)
docker-compose logs -f odoo
```

### Accessing the System

- **Odoo Web UI**: `http://localhost:8069`
- **Database**: `postgresql://odoo:odoo@localhost:5432/odoo`

### Initial Configuration

1. Create a new database:
   - Database name: `odoo`
   - Admin email: `admin@example.com`
   - Admin password: `admin`

2. Install Ask Management module:
   - Go to the Apps menu
   - Search for **"Ask Management"**
   - Click **Install**

## 💼 Business Scenarios

### 1. Salesperson Collects Customer Demand

```text
Customer: “We need 100 units of Product A and 50 units of Product B next week.”
Salesperson → Create Ask Order → Set Periodic Ask → Submit to system
```

### 2. System Auto Processing

```text
Every day at 23:59 → Cutoff job runs → Lock demands → Generate procurement suggestions
```

### 3. Procurement Decision

```text
Procurement Manager → Open Dashboard → Review total demand → Create Purchase Orders
```

### 4. Inventory Management

```text
Warehouse Manager → Receive purchased goods → Create reservations → Notify salespersons
```

### 5. Delivery Control

```text
Salesperson → Create Sales Order → Validate delivery → System checks reservation & permissions
```

## 🔧 Technical Details

### Data Model Design

- **Ask (`ask.ask`)**: Ask order master record, including customer, date, status, etc.
- **Ask Line (`ask.line`)**: Ask lines with product, quantity, warehouse, and other details
- **Reservation (`ask.reservation`)**: Reservation records controlling stock allocation and usage rights
- **Storage Fee (`ask.storage_fee`)**: Storage fee calculation records

### Access Control

- **Sales User**: Create and manage ask orders
- **Purchase User**: View procurement dashboard and create purchase orders
- **Warehouse User**: Manage stock reservations and deliveries
- **Administrator**: Full access

### Module Integrations

- **Inventory**: Extends delivery validation logic
- **Sales**: Links customers and sales orders
- **Purchase**: Integrates purchase order creation
- **Accounting**: Supports storage fee accounting

## 📊 Data Flow

```mermaid
graph TD
    A[Customer Demand] --> B[Create Ask Order]
    B --> C{Submit for Review}
    C -->|Yes| D[Daily Cutoff]
    C -->|No| B
    D --> E[Lock Demand]
    E --> F[Procurement Aggregation]
    F --> G[Procurement Decision]
    G --> H[Inventory Reservation]
    H --> I[Delivery Request]
    I --> J{Permission Check}
    J -->|Approved| K[Validate Delivery]
    J -->|Rejected| L[Permission Warning]
```

## 🧪 Test Cases

### Functional Tests

1. **Basic Flow**: Create Ask → Run cutoff → Procurement aggregation
2. **Reservation Control**: Create reservation → Validate delivery permission control
3. **Scheduled Jobs**: Manually trigger cutoff and verify state transitions
4. **Dashboard**: Validate data aggregation and procurement suggestions

### Performance Tests

- Support **1000+ concurrent users**
- Handle **100,000+ ask orders**
- Real-time data aggregation response time **< 2 seconds**

## 🔒 Security Features

- **Data Isolation**: Record-level access controlled by user groups
- **Operation Audit**: Full audit trail for all key operations
- **Permission Checks**: Multi-level permission checks for delivery validation
- **Data Integrity**: Database-level constraints and validation

## 📈 Extensibility

### Planned Features

- [ ] AI-based demand forecasting
- [ ] Mobile app support
- [ ] Advanced analytics reports
- [ ] Third-party system integration APIs

### Integration Capabilities

- **ERP Systems**: SAP, Oracle and other enterprise ERPs
- **E-commerce Platforms**: Taobao, JD, etc. data synchronization
- **Logistics Systems**: SF Express, YTO, etc. tracking integration

## 🤝 Contributing

### Development Setup

```bash
# Clone the development branch
git clone -b develop https://github.com/nio1112/my-odoo-apps.git

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest addons/odoo_ask/tests/
```

### Code Style

- Follow **Odoo official development guidelines**
- Use **ESLint** (for JS) and **Black** (for Python) for code formatting
- All unit tests must pass before committing
- Follow **Conventional Commits** specification for commit messages

## 📄 License

This project is licensed under the **LGPL-3.0** license. See the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

- **Project Home**: `https://github.com/nio1112/my-odoo-apps`
- **Issue Tracker**: `https://github.com/nio1112/my-odoo-apps/issues`
- **Email Support**: `453678080@qq.com`
- **Technical Docs**: [Detailed Documentation](addons/odoo_ask/README.md)

## 🎯 Changelog

### v19.0.1.1 (2025-11-13)

- ✨ Added Ask creation wizard
- 🔧 Optimized delivery validation logic
- 📊 Enhanced procurement dashboard
- 🐛 Fixed issues with scheduled jobs

### v19.0.1.0 (2025-11-01)

- 🎉 Initial release
- ✅ Implemented core ask management features
- ✅ Completed inventory reservation system
- ✅ Added Docker-based one-click deployment

---

⭐ If this project is helpful to you, please consider giving it a **Star**!


