import globaldb
import indicators
import latestcryptoprices
import latestcurrencyprices
import latestfutureprices
import latestindicesprices
import lateststockprices


def sync():
    max_date = globaldb.getMaxDate()
    print("updating stocks.............................................")
    lateststockprices.updatePrice(max_date)
    print("updating futures/commodity..................................")
    latestfutureprices.updatePrice(max_date)

    print("updating forex/currency.....................................")
    latestcurrencyprices.updatePrice(max_date)

    print("updating indices............................................")
    latestindicesprices.updatePrice(max_date)
    print("updating crypto.............................................")
    latestcryptoprices.updatePrice(max_date)

    print("updating indicators.............................................")
    indicators.update('latest')
