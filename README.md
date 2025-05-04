# Distributed Online Marketplace System

This project is a **distributed online marketplace platform** built using **Django** and **PostgreSQL**, designed to provide essential e-commerce functionalities through a scalable and modular architecture. It supports user account management, item listing, purchases, and secure financial transactions. The system also includes RESTful APIs and a distributed database model.

## Technology Stack

* **Backend:** Django (Python)
* **Database:** PostgreSQL (partitioned)
* **API Framework:** Django REST Framework (DRF)
* **Authentication:** Django built-in auth system
* **Architecture:** RESTful, modular, distributed schema design

## Core Features

### User Account Management

* User registration and login
* Authentication and session handling

### Product and Inventory Management

* Add, edit, and delete items for sale
* View and manage personal inventory

### Transactions and Payments

* Deposit funds into user wallet
* Purchase items listed by other users
* Automatic transfer of funds and item ownership

### Search and Discovery

* Search functionality to browse products listed by others

### Account Overview

* View account balance
* List of purchased items
* List of sold items
* Current inventory

### Reporting

* Generate reports for transaction history, sales, and purchases

### External Store Integration

* Provides a REST API interface that allows third-party stores to seamlessly integrate and list products from our platform onto theirs

## Implemented REST APIs

Three main functionalities are implemented using RESTful web services:

* User registration and login
* Product Listing via External API
* Deposit

These APIs follow standard REST conventions and can be tested through tools like Postman or cURL.

## API Documentation

The API documentation is available at [SALES\_Square/API](https://marketplace-production-ba97.up.railway.app/static/docs/salesquare_api_documentation.docx)

## Integration with External Stores

Third-party stores can integrate with our marketplace by:

1. Registering as an external partner by contacting us
2. Using our Product Listing API to sync inventory

## Screenshots

Below are sample screenshots of the system in use:

![Home Page](screenshots/home.png)
![User Dashboard](screenshots/dashboard.png)
![Product Listing](screenshots/product_list.png)

> *Ensure you place actual screenshots in a `screenshots/` directory in your repo or update the paths to match your project structure.*

## Getting Started

### Initial Deployment

1. Connect your GitHub repository to Railway
2. Configure all required environment variables
3. Set up persistent volumes
4. Trigger initial deployment

```bash
git push origin main
```

### Post-Deployment Setup

After successful deployment:

```bash
# Apply database migrations
railway run python manage.py migrate

# Create superuser (for admin access)
railway run python manage.py createsuperuser

# Load initial data (optional)
railway run python manage.py loaddata initial_data.json
```

## Monitoring and Maintenance

Railway provides:

* Real-time application logs
* Performance monitoring dashboards
* Automatic health checks (available at `/health/`)
* Resource utilization metrics

## Development Workflow

### CI/CD Pipeline

1. Code pushed to main branch triggers automated build
2. Test suite runs (pytest)
3. If tests pass:

   * Docker image is built
   * New version is deployed to production
   * Database migrations run automatically

### Local Development

To mirror the Railway environment locally:

```bash
# Install dependencies
pip install -r SALES_square/requirements.txt

# Run with Railway environment
railway run python manage.py runserver
```

## Distributed Database Design

The system uses **PostgreSQL** with a distributed partitioning model to improve scalability and performance:

* Logical partitioning of tables (e.g., by user or category)
* Optimized for high-volume reads/writes
* Schema supports horizontal scalability and data isolation

## Support and Troubleshooting

### Common issues and solutions:

1. Database Connection Issues

   * Verify DATABASE\_URL format
   * Check connection limits in PostgreSQL settings

2. Media Upload Problems

   * Confirm persistent volume is mounted
   * Verify file permissions

3. Performance Optimization

   * Enable Redis caching
   * Review query optimization
   * Consider adding more replicas

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please [contact us](https://marketplace-production-ba97.up.railway.app/contactus) or open an issue in the repository.
