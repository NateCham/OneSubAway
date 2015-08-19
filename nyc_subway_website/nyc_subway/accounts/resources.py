class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ('get', 'post', 'put', 'delete', 'patch')
        filtering = { "id" : ALL }
