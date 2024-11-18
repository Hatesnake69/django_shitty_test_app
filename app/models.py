from django.db import models


class WbTaskModel(models.Model):
    objects = models.Manager()  # Add the default manager
    employee = models.CharField(max_length=256, blank=False, null=False)
    account = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"assemble task {self.account} {self.employee} "

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "wb_tasks"


class WbSupplyModel(models.Model):
    objects = models.Manager()  # Add the default manager
    wb_supply_id = models.BigIntegerField(unique=True, blank=False, null=False)
    task = models.OneToOneField(
        "app.WbTaskModel", on_delete=models.CASCADE, null=True, blank=True, related_name="supply"
    )

    def __str__(self):
        return f"supply {self.wb_supply_id}"

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "wb_supplies"


class WbOrderModel(models.Model):
    objects = models.Manager()  # Add the default manager
    wb_id = models.BigIntegerField(unique=True, blank=False, null=False)
    supply = models.ForeignKey(
        "app.WbSupplyModel", on_delete=models.CASCADE, null=True, blank=True, related_name="order"
    )
    qr_code = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"order {self.wb_id}"

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "wb_orders"


class WbOrderProductModel(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        "app.WbOrderModel", on_delete=models.CASCADE, related_name="order_product", blank=False, null=False
    )
    name = models.CharField(max_length=256, blank=False, null=False)
    code = models.CharField(unique=True, max_length=256, default=None)
    quantity = models.IntegerField(blank=False, null=False)
    wb_sgtin = models.CharField(default=None, max_length=256, null=True, blank=True)
    has_honest_sign = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"{self.name} {self.quantity}шт."

    class Meta:
        db_table = "wb_order_products"
