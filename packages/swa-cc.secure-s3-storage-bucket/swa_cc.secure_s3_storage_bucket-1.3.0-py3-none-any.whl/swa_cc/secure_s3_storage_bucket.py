from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_iam as iam,
    aws_events as events
)
import datetime

class S3StorageBucketStack(core.Stack):
    """
    Builds the compliant S3 bucket.

    Parameters
    ----------
    scope : aws_cdk.core.Construct
        Parent of this stack, usually a Program instance.
    id : str
        The name of the CloudFormation stack.

    Attributes
    -------
    bucket_arn : aws_cdk.core.Token
        The arn of the bucket that will be created

    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        encrypytion = s3.BucketEncryption
        removal_policy = core.RemovalPolicy
        kms_key = kms.Key.from_key_arn(self, id, key_arn="swa_" + str(core.Aws.ACCOUNT_ID) + "_kms")
        public_access = s3.BlockPublicAccess

        bucket = s3.Bucket(self,
                    id+"s3Bucket",
                    block_public_access=public_access.BLOCK_ALL, bucket_name=id.lower(), cors=None,
                    encryption=encrypytion.KMS, encryption_key=kms_key, lifecycle_rules=None,
                    metrics=None, public_read_access=None, removal_policy=removal_policy.DESTROY,
                    versioned=None)

        principal = iam.AnyPrincipal()

        bucket_policy = iam.PolicyStatement(actions=['s3:*'],
                        conditions={"Bool" : {"aws:SecureTransport":"false"}},
                        effect=iam.Effect.DENY,
                        principals= [principal],
                        resources=[bucket.bucket_arn + "/*"])
        bucket.add_to_resource_policy(bucket_policy)
        self.__bucket = bucket
        self.bucket_arn = bucket.bucket_arn
        self.encryption_key = bucket.encryption_key
        self.policy = bucket.policy
        self.bucket_name = bucket.bucket_name

    def add_lifecycle_rule(self, rule, abort_incomplete_multipart_upload_after: core.Duration = None, enabled: bool = None, #NOSONAR
                            expiration: core.Duration = None, expiration_date: datetime = None, id: str = None, noncurrent_version_expiration: core.Duration = None,
                            noncurrent_version_transitions: [s3.NoncurrentVersionTransition] = None, prefix: str = None, tag_filters: {str, any} = None,
                            transitions: [s3.Transition] = None):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_lifecycle_rule(rule = rule, abort_incomplete_multipart_upload_after=abort_incomplete_multipart_upload_after, enabled=enabled,
                                        expiration=expiration, expiration_date=expiration_date, id=id, noncurrent_version_expiration=noncurrent_version_expiration,
                                        noncurrent_version_transitions=noncurrent_version_transitions, prefix=prefix, tag_filters=tag_filters, transitions=transitions)

    def add_metric(self, metric, id: str, prefix: str = None, tag_filters: {str, str} = None):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_metric(metric = metric, id = id, prefix = prefix, tag_filters = tag_filters)

    def add_object_created_notification(self, dest: s3.IBucketNotificationDestination, filters: s3.NotificationKeyFilter):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_object_created_notification(dest = dest, filters = filters)

    def add_object_removed_notificationself(self, dest: s3.IBucketNotificationDestination, filters: s3.NotificationKeyFilter):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_object_removed_notification(dest = dest, filters = filters)

    def add_event_notification(self, event: s3.EventType, dest: s3.IBucketNotificationDestination, filters: s3.NotificationKeyFilter):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_event_notification(event, dest, filters)
        self.policy = self.__bucket.policy

    def add_to_resource_policy(self, policy: iam.PolicyStatement):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        self.__bucket.add_to_resource_policy(policy)
        self.policy = self.__bucket.policy

    def arn_for_objects(self, key_pattern: str):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        return self.__bucket.arn_for_objects(key_pattern = key_pattern)

    def on_cloud_trail_event(self, id: str, options, paths: [str] = None, description: str = None, event_pattern: events.EventPattern = None, #NOSONAR
                                rule_name: str = None, target: events.IRuleTarget = None):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        return self.__bucket.on_cloud_trail_event(id = id, options = options, paths = paths, description = description, event_pattern = event_pattern,
                                                    rule_name = rule_name, target = target)

    def on_cloud_trail_put_object(self, id: str, options, paths: [str] = None, description: str = None, event_pattern: events.EventPattern = None, #NOSONAR
                                    rule_name: str = None, target: events.IRuleTarget = None):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        return self.__bucket.on_cloud_trail_put_object(id = id, options = options, paths = paths, description = description, event_pattern = event_pattern,
                                                        rule_name = rule_name, target = target)

    def url_for_object(self, key = None):
        """
        Please See documentation at https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        """
        return self.__bucket.url_for_object(key = key)