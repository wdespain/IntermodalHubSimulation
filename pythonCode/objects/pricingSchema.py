#Handles and return the pricing information

class PricingSchema():

	def __init__(self, b, sc, wc, ps, ws, et):
		self.baseCharge = b #54$
		self.summerChargeKWH = sc #14.62$
		self.winterChargeKWH = wc #10.91$
		self.peakSummerChargeKWH = ps #.038127$
		self.peakWinterChargeKWH = ws #.035143$
		self.peakEnergyThreashold = et #2300