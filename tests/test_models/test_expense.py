from wallet.models import Category, Expense


def test_model_delete_category(self):
    # test when expense's category was deleted, should change expenses's
    # category to the default category
    Expense.objects.create(category=self.category, amount=11, owner=self.user)
    self.assertEqual(Expense.objects.count(), 1)
    self.category.delete()
    self.assertEqual(Expense.objects.first().category, None)
