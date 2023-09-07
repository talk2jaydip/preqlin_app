
**Design 2**

Assume Follwing:
- An Amazon Elastic Compute Cloud (EC2) instance to host the machine learning models.
- An Amazon Elastic Container Service (ECS) cluster to run the Lambda function.
- An Amazon Simple Queue Service (SQS) queue to buffer the documents before they are processed by the Lambda function.

**Design**

-   An Amazon Simple Notification Service (SNS) topic to receive the documents.
-   An Amazon Lambda function to extract the text from the documents and send it to the machine learning models.
-   Three Amazon SageMaker models: one to identify whether the document is about politics, one to identify the language of the document, and one to identify company mentions in the headline.
-   An Amazon DynamoDB table to store the processed documents.

The documents will be sent to the SNS topic every 1 minute. 
The Lambda function would then be triggered by the SNS topic and would extract the text from the documents. 
The text would then be sent to the three SageMaker models to be enriched. The enriched documents would then be stored in the DynamoDB table.

** Improvements**

The initial design can be improved in a number of ways:
-   The SageMaker models could be deployed in a production-ready environment. This would make them more reliable and scalable.
-   The DynamoDB table could be configured to allow for more concurrent reads and writes. This would improve performance and availability.

**Justification**

The AWS services used in this architecture are suited for the task of enriching documents with machine learning models. 
SNS is a scalable and reliable way to receive and distribute messages. 
Lambda is a serverless compute service that can be used to process the documents and send them to the machine learning models. 
SageMaker is a managed machine learning service that provides a variety of pre-trained models that can be used to enrich documents. 
DynamoDB is a NoSQL database that is well-suited for storing large amounts of data.

**Limitations and  Improvements**

The initial design has a number of limitations, such as the fact that it is not scalable and does not allow for concurrent reads and writes. These limitations can be addressed by making the following improvements:

-   The Lambda function could be made more scalable by using a containerized approach. This would allow the function to be scaled up or down as needed.
-   The DynamoDB table could be configured to allow for more concurrent reads and writes. This would improve performance and availability.

