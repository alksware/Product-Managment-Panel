import sqlite3
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from productUI import Ui_MainWindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

con = sqlite3.connect("applicationDatabase.db")
cursor = con.cursor()


def createTable():
    cursor.execute("""CREATE TABLE IF NOT EXISTS applicationTable (
        productCode INT,
        productName TEXT,
        productAmount INT,
        productPrice INT,
        productDescription TEXT,
        productCategory TEXT,
        productBrand TEXT
    )""")
    con.commit()


def addProduct():
    productCode = int(ui.productCode.text())
    productName = ui.productName.text()
    productAmount = int(ui.productAmount.text())
    productPrice = int(ui.productPrice.text())
    productDescription = ui.productDescription.text()
    productCategory = ui.cmdCatagory.currentText()
    productBrand = ui.cmbProduct.currentText()

    try:
        add = "insert into applicationTable(productCode,productName,productAmount,productPrice,productDescription," \
              "productCategory,productBrand) values(?,?,?,?,?,?,?)"
        cursor.execute(add, (
        productCode, productName, productAmount, productPrice, productDescription, productCategory, productBrand))
        con.commit()
        ui.statusbar.showMessage("Product added", 5000)
    except Exception as e:
        ui.statusbar.showMessage("Product couldn't be added", 5000)
        raise e


def list():
    ui.tableList.clear()
    ui.tableList.setHorizontalHeaderLabels(["productCode", "productName", "productAmount", "productPrice",
                                            "productDescription", "productCategory", "productBrand"])
    Query = "select *  from applicationTable "
    cursor.execute(Query)
    # enemerute : bir listenin elemanlarını indexler
    for indexColumn, saveNo in enumerate(cursor):
        for indexRow, saveNo2 in enumerate(saveNo):
            ui.tableList.setItem(indexColumn, indexRow, QTableWidgetItem(str(saveNo2)))

def listAccordingToCatagory():
    catagory = ui.cmbListAsCatagory.currentText()
    Query = ("select * from applicationTable where productCategory = ?", (catagory,))
    cursor.execute(*Query)  # Tuple olarak aktarıldığından * kullanarak çözüyoruz.
    ui.tableList.clear()
    for indexColumn, saveNo in enumerate(cursor):
        for indexRow, saveNo2 in enumerate(saveNo):
            ui.tableList.setItem(indexColumn, indexRow, QTableWidgetItem(str(saveNo2)))

from PyQt5.QtWidgets import QMessageBox

# ... (Önceki kodlarınız) ...

def deleteProduct():
    product = ui.tableList.selectedItems()
    if not product:
        ui.statusbar.showMessage("Please select a product to delete.", 5000)
        return

    productD = product[0].text()

    # Onay iletişim kutusunu oluştur.
    confirm_message = QMessageBox.question(window, "Confirm", "Selected Product Delete?", QMessageBox.Yes | QMessageBox.No)

    # Kullanıcı evet'i seçtiyse ürünü sil.
    if confirm_message == QMessageBox.Yes:
        Query = ("delete from applicationTable where productCode = ?", (productD,))
        cursor.execute(*Query)  # Silme işlemini gerçekleştir.
        con.commit()  # Değişiklikleri veritabanına uygula.

        # Kullanıcıya geri bildirim ver.
        ui.statusbar.showMessage("Product Deleted", 5000)

        # Tabloyu güncelle.
        list()  # Tüm ürünleri tekrar listele
def updateProduct():
    message = QMessageBox.question(window, "Update Confirmation",
                                   "Are you sure you want to update this data?",
                                   QMessageBox.Yes | QMessageBox.No)

    if message == QMessageBox.Yes:
        try:
            productCode = int(ui.productCode.text())
            productName = ui.productName.text()
            productAmount = int(ui.productAmount.text())
            productPrice = int(ui.productPrice.text())
            productDescription = ui.productDescription.text()
            productCategory = ui.cmdCatagory.currentText()
            productBrand = ui.cmbProduct.currentText()

            if productName == "" and productPrice == "" and productAmount == "" and productDescription == "" and productBrand == "":
                cursor.execute("UPDATE applicationTable SET productCategory = ? WHERE productCode = ?", (productCategory, productCode))

            elif productName == "" and productPrice == "" and productAmount == "" and productDescription == "" and productCategory == "":
                cursor.execute("UPDATE applicationTable SET productBrand = ? WHERE productCode = ?", (productBrand, productCode))

            elif productName == "" and productPrice == "" and productAmount == "" and productBrand == "" and productCategory == "":
                cursor.execute("UPDATE applicationTable SET productDescription = ? WHERE productCode = ?", (productDescription, productCode))

            elif productName == "" and productPrice == "" and productDescription == "" and productBrand == "" and productCategory == "":
                cursor.execute("UPDATE applicationTable SET productAmount = ? WHERE productCode = ?", (productAmount, productCode))

            elif productName == "" and productAmount == "" and productDescription == "" and productBrand == "" and productCategory == "":
                cursor.execute("UPDATE applicationTable SET productPrice = ? WHERE productCode = ?", (productPrice, productCode))

            elif productAmount == "" and productPrice == "" and productDescription == "" and productBrand == "" and productCategory == "":
                cursor.execute("UPDATE applicationTable SET productName = ? WHERE productCode = ?", (productName, productCode))

            else:
                cursor.execute("UPDATE applicationTable SET productName = ?, productAmount = ?, productPrice = ?, productDescription = ?, productBrand = ?, productCategory = ? WHERE productCode = ?",
                               (productName, productAmount, productPrice, productDescription, productBrand, productCategory, productCode))

            con.commit()
            list()
            ui.statusbar.showMessage("Record Updated Successfully")
        except Exception as error:
            ui.statusbar.showMessage("Error occurred while updating the record: " + str(error))
    else:
        ui.statusbar.showMessage("Update Cancelled")

ui.addProductButton.clicked.connect(addProduct)
ui.listProductButton.clicked.connect(list)
ui.listProductAsCatagory.clicked.connect(listAccordingToCatagory)
ui.deleteProductButton.clicked.connect(deleteProduct)
ui.updateProductButton.clicked.connect(updateProduct)
window.show()
sys.exit(app.exec_())
