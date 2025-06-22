balance_sheet_mapping = {
        "EQUITY AND LIABILITIES": {
            "Shareholder's Fund": {
                "Share capital": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row1[0].ShareCap[0]",
                                  "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row1[0].ShareCapP[0]"),
                "Reserves and surplus": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row2[0].ResSur[0]",
                                         "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row2[0].ResSurP[0]"),
                "Money received against share warrants": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row3[0].ShareWarrant[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row3[0].ShareWarrantP[0]")
            },
            "Share application money pending allotment": (
                "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row4[0].ShareAllot[0]",
                "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row4[0].ShareAllotP[0]"),
            "Non-current liabilities": {
                "Long term borrowings": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row6[0].LongTerm[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row6[0].LongTermP[0]"),
                "Deferred tax liabilities (net)": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row7[0].DefLiabl[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row7[0].DefLiablP[0]"),
                "Other long term liabilities": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row8[0].LongLiabl[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row8[0].LongLiablP[0]"),
                "Long term provisions": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row9[0].LongProv[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row9[0].LongProvP[0]")
            },
            "Current liabilities": {
                "Short term borrowings": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row11[0].ShortBorrow[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row11[0].ShortBorrowP[0]"),
                "Trade payables": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row12[0].Trade[0]",
                                   "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row12[0].TradeP[0]"),
                "Other current liabilities": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row13[0].CurrentLiabl[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row13[0].CurrentLiablP[0]"),
                "Short term provisions": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row14[0].ShortProv[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row14[0].ShortProvP[0]")
            },
            "Total": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row15[0].Total[0]",
                      "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row15[0].TotalP[0]")
        },
        "ASSETS": {
            "Non-current assets": {
                "Fixed assets": {
                    "Tangible assets": (
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row19[0].TangAsset[0]",
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row19[0].TangAssetP[0]"),
                    "Intangible assets": (
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row20[0].IntangAsset[0]",
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row20[0].IntangAssetP[0]"),
                    "Capital work-in-progress": (
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row21[0].CapWork[0]",
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row21[0].CapWorkP[0]"),
                    "Intangible assets under development": (
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row22[0].IntangAsset[0]",
                        "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row22[0].IntangAssetP[0]")
                },
                "Non-current Investments": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row23[0].NonCurrent[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row23[0].NonCurrentP[0]"),
                "Deferred tax assets (net)": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row24[0].DefTax[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row24[0].DefTaxP[0]"),
                "Long term loans and advances": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row25[0].LongLoan[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row25[0].LongLoanP[0]"),
                "Other non-current assets": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row26[0].OtherAsset[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row26[0].OtherAssetP[0]")
            },
            "Current assets": {
                "Current Investment": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row28[0].Current[0]",
                                       "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row28[0].CurrentP[0]"),
                "Inventories": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row29[0].Inventory[0]",
                                "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row29[0].InventoryP[0]"),
                "Trade receivables": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row30[0].Trade[0]",
                                      "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row30[0].TradeP[0]"),
                "Cash and cash equivalents": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row31[0].Cash[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row31[0].CashP[0]"),
                "Short term loans and advances": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row32[0].ShortLoan[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row32[0].ShortLoanP[0]"),
                "Other current assets": (
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row33[0].OtherAsset[0]",
                    "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row33[0].OtherAssetP[0]")
            },
            "Total": ("data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row34[0].Total[0]",
                      "data[0].FormAOC4_Dtls[0].BalanceSheet1_PartB[0].Table6[0].Row34[0].TotalP[0]")
        }
    }

long_term_borrowing_mapping = {
    "Bonds/ debentures": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row2[0].Bonds[0]",
                          "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row2[0].BondsP[0]"),
    "Term Loans": {
        "From banks": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row4[0].Banks[0]",
                       "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row4[0].BanksP[0]"),
        "From other parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row5[0].Other[0]",
                               "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row5[0].OtherP[0]")
    },
    "Deferred payment liabilities": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row6[0].Deferred[0]",
                                     "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row6[0].DeferredP[0]"),
    "Deposits": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row7[0].Deposits[0]",
                 "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row7[0].DepositsP[0]"),
    "Loans and advances from related parties": (
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row8[0].Loans[0]",
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row8[0].LoansP[0]"),  # Corrected key
    "Long term maturities of financial lease Obligations": (
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row14[0].Maturities[0]",
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row14[0].MaturitiesP[0]"),
    "Other loans & advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row15[0].Others[0]",
                               "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row15[0].OthersP[0]"),
    "Total long term borrowings (unsecured)": (
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row16[0].Total[0]",
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row16[0].TotalP[0]"),
    "Out of above total, aggregate amount guaranteed by directors": (
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row18[0].Aggregate[0]",
        "data[0].FormAOC4_Dtls[0].BalanceSheet2_A[0].Table8[0].Row18[0].AggregateP[0]")
}

short_term_borrowing_mapping = {
        "Loans repayable on demand": {
            "From banks": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row4[0].Banks[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row4[0].BanksP[0]"),
            "From other parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row5[0].Other[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row5[0].OtherP[0]")
        },
        "Loans and advances from related parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row8[0].Advances[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row8[0].AdvancesP[0]"),
        "Deposits": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row14[0].Deposits[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row14[0].DepositsP[0]"),
        "Other loans and advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row15[0].Others[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row15[0].OthersP[0]"),
        "Total short term borrowings (unsecured)": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row16[0].Total[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row16[0].TotalP[0]"),
        "Out of above total, aggregate amount guaranteed by directors": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row18[0].Aggregate[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_B[0].Table9[0].Row18[0].AggregateP[0]")
    }

long_term_loan_unsecured_mapping = {
        "Capital advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row2[0].Capital[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row2[0].CapitalP[0]"),
        "Security deposits": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row3[0].Security[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row3[0].SecurityP[0]"),
        "Loans and advances to other related parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row4[0].Loans[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row4[0].LoansP[0]"),
        "Other loans and advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row5[0].Others[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row5[0].OthersP[0]"),
        "Total long term loan and advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row6[0].Total[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row6[0].TotalP[0]"),
        "Less: Provision/ allowance for bad and doubtful loans and advances": {
            "From related parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row8[0].Parties[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row8[0].PartiesP[0]"),
            "From others": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row14[0].Others[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row14[0].OthersP[0]")
        },
        "Net long term loan and advances (unsecured, considered good)": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row16[0].Total[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row16[0].TotalP[0]"),
        "Loans and advances due by directors/ other officers of the company": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row18[0].Aggregate[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_C[0].Table8[0].Row18[0].AggregateP[0]")
    }

long_term_loan_doubtful_mapping = {
        "Capital advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row2[0].Capital[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row2[0].CapitalP[0]"),
        "Security deposits": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row3[0].Security[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row3[0].SecurityP[0]"),
        "Loans and advances to other related parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row4[0].Loans[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row4[0].LoansP[0]"),
        "Other loans and advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row5[0].Others[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row5[0].OthersP[0]"),
        "Total long term loan and advances": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row6[0].Total[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row6[0].TotalP[0]"),
        "Less: Provision/ allowance for bad and doubtful loans and advances": {
            "From related parties": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row8[0].Parties[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row8[0].PartiesP[0]"),
            "From others": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row14[0].Others[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row14[0].OthersP[0]")
        },
        "Net long term loan and advances (doubtful)": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row16[0].Total[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row16[0].TotalP[0]"),
        "Loans and advances due by directors/ other officers of the company": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row18[0].Aggregate[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_D[0].Table9[0].Row18[0].AggregateP[0]") # The provided resulted_dictionary has empty strings for these, so they will remain None
    }

trade_receivable_mapping = {
        "Secured, considered good": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row3[0].SecuredCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row3[0].SecuredPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row3[0].SecuredCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row3[0].SecuredPwi[0]")
        },
        "Unsecured, considered good": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row4[0].UnsecuredCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row4[0].UnsecuredPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row4[0].UnsecuredCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row4[0].UnsecuredPwi[0]")
        },
        "Doubtful": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row5[0].DoubtfulCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row5[0].DoubtfulPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row5[0].DoubtfulCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row5[0].DoubtfulPwi[0]")
        },
        "Total trade receivables": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row6[0].TotalCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row6[0].TotalPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row6[0].TotalCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row6[0].TotalPwi[0]")
        },
        "Less: Provision/ allowance for bad and doubtful debts": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row7[0].AggregateCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row7[0].AggregatePex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row7[0].AggregateCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row7[0].AggregatePwi[0]")
        },
        "Net trade receivables": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row8[0].TotalCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row8[0].TotalPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row8[0].TotalCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row8[0].TotalPwi[0]")
        },
        "Debt due by directors/ others officers of the company": {
            "Exceeding six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row14[0].DebtCex[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row14[0].DebtPex[0]"),
            "Within six months": ("data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row14[0].DebtCwi[0]", "data[0].FormAOC4_Dtls[0].BalanceSheet2_E[0].Table10[0].Row14[0].DebtPwi[0]")
        }
    }

financial_parameters_mapping = {
        "Amount of issue allotted for contracts without payment received in cash during reporting periods": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row1[0].AmountContract[0]",
        "Share application money given during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row2[0].ShareMoney[0]",
        "Share application money received during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row4[0].ShareMoneyReceive[0]",
        "Share application money received and due for refund": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row5[0].ShareMoneyRefund[0]",
        # The template has "Share application money received and due for refund", but the data has "ShareMoneyReceive" and "ShareMoneyRefund".
        # Assuming "ShareMoneyReceive" is the value for "Share application money received and due for refund" as it has a non-zero value, and "ShareMoneyRefund" is a separate detail.
        # If "Share application money received and due for refund" needs to be a sum or specific calculation, it needs clarification.
        # For now, mapping directly based on the provided JSON structure.
        "Paid-up capital held by foreign company": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row6[0].PaiUp[0]",
        "Paid-up capital held by foreign holding company and/ or through its subsidiaries": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row7[0].PaiUpSub[0]",
        "Number of shares bought back during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row8[0].ShareNum[0]",
        "Deposits accepted or renewed during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11[0].Row9[0].Deposits[0]",
        "Deposits matured and claimed but not paid during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row1[0].DepositsNotPaid[0]",
        "Deposits matured and claimed but not paid": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row2[0].DepositsMatured[0]",
        "Deposits matured, but not claimed": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row3[0].DepositsNoClaim[0]",
        "Unclaimed matured debentures": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row4[0].UnclaimDeben[0]",
        "Debentures claimed but not paid": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row5[0].ClaimedDeben[0]",
        "Interest on deposits accrued and due but not paid": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row6[0].Interest[0]",
        "Unpaid dividend": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row7[0].Unpaid[0]",
        "Investment in subsidiary companies": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row8[0].Subsidiary[0]",
        "Investment in government companies": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row9[0].GovtSubsidiary[0]",
        "Capital Reserves": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row10[0].Capital[0]",
        "Amount due for transfer to Investor Education and Protection Fund (IEPF)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row11[0].Amount[0]",
        "Inter- corporate deposits": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row12[0].Deposits[0]",
        "Gross value of transaction as per AS 18 (if applicable)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row13[0].GrossVal[0]",
        "Capital subsidies/ grants received from government authority(ies)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row14[0].GrantsRec[0]",
        "Calls unpaid by directors": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row15[0].Directors[0]",
        "Calls unpaid by others": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row16[0].Others[0]",
        "Forfeited shares (amount originally paid-up)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row17[0].Shares[0]",
        "Forfeited shares reissued": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row18[0].SharesIssued[0]",
        "Borrowing from foreign institutional agencies": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row19[0].ForeignInst[0]",
        "Borrowing from foreign government": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row20[0].ForeignAgency[0]",
        "Inter-corporate borrowings - secured": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_1[0].Row21[0].SecBorrow[0]",
        "Inter-corporate borrowings - unsecured": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row22[0].UnsecBorrow[0]",
        "Commercial Paper": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row23[0].Commercial[0]",
        "Conversion of warrants into equity shares during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row24[0].EqutiyWarrants[0]",
        "Conversion of warrants into preference shares during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row25[0].PreferenceWarrants[0]",
        "Conversion of warrants into debentures during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row26[0].DebtWarrants[0]",
        "Warrants issued during the reporting period (Foreign Currency)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row27[0].ForeignWarrants[0]",
        "Warrants issued during the reporting period (In Rupees)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row28[0].IndianWarrants[0]",
        "Default in payment of short term borrowings and interest thereon": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row29[0].ShortDefault[0]",
        "Default in payment of long term borrowings and interest thereon": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row30[0].LongDefault[0]",
        "Whether any operating lease has been converted to financial lease or vice versa": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row31[0].FinancLease[0]",
        "Provide details of such conversion": "data[0].FormAOC4_Dtls[0].BalanceSheet3_1[0].Table11_2[0].Row32[0].Details[0].Othr[0]",
        "Net worth of company": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row33[0].NetWorth[0]",
        "Number of shareholders to whom shares allotted under private placement during the reporting period": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row34[0].Shareholders[0]",
        "Secured loans": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row35[0].TextField1[0]",
        "Gross fixed assets (including intangible assets)": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row36[0].TextField2[0]",
        "Depreciation and amortization": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row37[0].TextField3[0]",
        "Miscellaneous expenditure to the extent not written off or adjusted": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row38[0].TextField4[0]",
        "Unhedged Foreign Exchange Exposure": "data[0].FormAOC4_Dtls[0].BalanceSheet3_2[0].Table11[0].Row39[0].ForeignExposure[0]"
    }

share_capital_raised_mapping = {
        "Public issue": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row2[0].NumericField1[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row2[0].NumericField2[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row2[0].NumericField3[0]"
        },
        "Bonus issue": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row3[0].NumericField4[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row3[0].NumericField5[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row3[0].NumericField6[0]"
        },
        "Right issue": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row4[0].NumericField7[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row4[0].NumericField8[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row4[0].NumericField9[0]"
        },
        "Private placement arising out of conversion of debentures or preference shares": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row5[0].PrivatePlace[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row5[0].NumericField10[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row5[0].NumericField11[0]"
        },
        "Other private placement": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row6[0].OtherPrivate[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row6[0].NumericField12[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row6[0].NumericField13[0]"
        },
        "Preferential allotment arising out of conversion of debentures or preference shares": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row7[0].NumericField14[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row7[0].NumericField15[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row7[0].NumericField16[0]"
        },
        "Other preferential allotment": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row8[0].NumericField17[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row8[0].NumericField18[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row8[0].NumericField19[0]"
        },
        "Employee Stock Option Plan (ESOP)": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row14[0].NumericField20[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row14[0].NumericField21[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row14[0].NumericField22[0]"
        },
        "Others": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row16[0].NumericField23[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row16[0].NumericField24[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row16[0].NumericField25[0]"
        },
        "Total amount of share capital raised during the reporting period": {
            "Equity Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row18[0].NumericField26[0]",
            "Preference Shares": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row18[0].NumericField27[0]",
            "Total": "data[0].FormAOC4_Dtls[0].BalanceSheet4[0].Table8[0].Row18[0].NumericField28[0]"
        }
    }

profit_and_loss_mapping = {
  "PROFIT AND LOSS": {
    "Revenue from operations": {
      "Domestic turnover": {
        "Sales of goods manufactured": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row3[0].NumericField31[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row3[0].NumericField32[0]"
        },
        "Sales of goods traded": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row4[0].NumericField33[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row4[0].NumericField34[0]"
        },
        "Sales or supply of services": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row5[0].NumericField35[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row5[0].NumericField36[0]"
        }
      },
      "Export turnover": {
        "Sales of goods manufactured": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row7[0].NumericField37[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row7[0].NumericField38[0]"
        },
        "Sales of goods traded": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row8[0].NumericField39[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row8[0].NumericField40[0]"
        },
        "Sales or supply of services": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row9[0].NumericField41[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row9[0].NumericField42[0]"
        }
      },
      "Other income": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row10[0].NumericField43[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row10[0].NumericField44[0]"
      },
      "Total Revenue (I+II)": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row11[0].NumericField45[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row11[0].NumericField46[0]"
      }
    },
    "Expenses": {
      "Cost of material consumed": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row13[0].NumericField47[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row13[0].NumericField48[0]"
      },
      "Purchases of stock in trade": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row14[0].NumericField49[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row14[0].NumericField50[0]"
      },
      "Changes in inventories of": {
        "Finished goods": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15[0].NumericField51[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15[0].NumericField52[0]"
        },
        "Work-in-progress": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15_A1[0].NumericField53[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15_A1[0].NumericField54[0]"
        },
        "Stock in trade": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15_A2[0].NumericField55[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row15_A2[0].NumericField56[0]"
        }
      },
      "Employee benefit Expense": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row16[0].NumericField57[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row16[0].NumericField58[0]"
      },
      "Management remuneration": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row17[0].NumericField59[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row17[0].NumericField60[0]"
      },
      "Payment to Auditors": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row18[0].NumericField61[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row18[0].NumericField62[0]"
      },
      "Insurance expenses": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row19[0].NumericField63[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row19[0].NumericField64[0]"
      },
      "Power and fuel": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row20[0].NumericField65[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row20[0].NumericField66[0]"
      },
      "Finance costs": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row21[0].NumericField67[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row21[0].NumericField68[0]"
      },
      "Depreciation and Amortisation": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row22[0].NumericField69[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row22[0].NumericField70[0]"
      },
      "Other expenses": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row23[0].NumericField71[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row23[0].NumericField72[0]"
      },
      "Total expenses": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row24[0].NumericField73[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row24[0].NumericField74[0]"
      }
    },
    "Profit before exceptional and extraordinary items and tax (III-IV)": {
      "Exceptional items": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row25[0].NumericField75[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row25[0].NumericField76[0]"
      },
      "Profit before extraordinary items and tax (V-VI)": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row26[0].NumericField77[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row26[0].NumericField78[0]"
      },
      "Extraordinary items": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row27[0].NumericField79[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row27[0].NumericField80[0]"
      },
      "Profit before tax (VII-VIII)": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row28[0].NumericField81[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row28[0].NumericField82[0]"
      },
      "Tax Expense": {
        "Current tax": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row31[0].NumericField85[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row31[0].NumericField86[0]"
        },
        "Deferred tax": {
          "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row32[0].NumericField87[0]",
          "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row32[0].NumericField88[0]"
        }
      }
    },
    "Profit/(Loss) for the period from continuing operations (IX-X)": {
      "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row33[0].NumericField89[0]",
      "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row33[0].NumericField90[0]"
    },
    "Profit/(Loss) from discontinuing operations": {
      "Profit/(loss) from discontinuing operations": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row34[0].NumericField91[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row34[0].NumericField92[0]"
      },
      "Tax expense of discontinuing operations": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row35[0].NumericField93[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row35[0].NumericField94[0]"
      },
      "Profit/(Loss) from discontinuing operations (after tax) (XII-XIII)": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row36[0].NumericField95[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row36[0].NumericField96[0]"
      }
    },
    "Profit/ (Loss) (XI+XIV)": {
      "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row37[0].NumericField97[0]",
      "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_1[0].Table6[0].Row37[0].NumericField98[0]"
    },
    "Earnings per equity share before extraordinary items": {
      "Basic": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row39[0].NumericField102[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row39[0].NumericField100[0]"
      },
      "Diluted": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row40[0].NumericField99[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row40[0].NumericField101[0]"
      }
    },
    "Earnings per equity share after extraordinary items": {
      "Basic": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row42[0].NumericField106[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row42[0].NumericField105[0]"
      },
      "Diluted": {
        "Current Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row43[0].NumericField104[0]",
        "Previous Period": "data[0].FormAOC4_Dtls[0].Segment2_table[0].Table6[0].Row43[0].NumericField103[0]"
      }
    }
  }
}

earnings_in_foreign_exchange_mapping = {
    "Export of goods calculated on FOB basis": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row2[0].NumericField107[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row2[0].NumericField108[0]"
    },
    "Interest and dividend": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row3[0].NumericField109[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row3[0].NumericField110[0]"
    },
    "Royalty": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row4[0].NumericField111[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row4[0].NumericField112[0]"
    },
    "Know-how": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row5[0].NumericField113[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row5[0].NumericField114[0]"
    },
    "Professional and consultation fees": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row6[0].NumericField115[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row6[0].NumericField116[0]"
    },
    "Other income": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row7[0].NumericField117[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row7[0].NumericField118[0]"
    },
    "Total Earning in Foreign Exchange": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row8[0].NumericField119[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2A[0].Table9[0].Row8[0].NumericField120[0]"
    }
  }

expenditure_in_foreign_exchange_mapping = {
    "Import of goods calculated on CIF basis": {
      "Raw material": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row3[0].NumericField121[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row3[0].NumericField122[0]"
      },
      "Component and spare parts": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row4[0].NumericField123[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row4[0].NumericField124[0]"
      },
      "Capital goods": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row5[0].NumericField125[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row5[0].NumericField126[0]"
      }
    },
    "Expenditure on account of": {
      "Royalty": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row7[0].NumericField129[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row7[0].NumericField130[0]"
      },
      "Know-how": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row8[0].NumericField131[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row8[0].NumericField132[0]"
      },
      "Professional and consultation fees": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row9[0].NumericField133[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row9[0].NumericField134[0]"
      },
      "Interest": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row10[0].NumericField135[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row10[0].NumericField136[0]"
      },
      "Other matters": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row11[0].NumericField137[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row11[0].NumericField138[0]"
      },
      "Dividend paid": {
        "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row12[0].NumericField139[0]",
        "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row12[0].NumericField140[0]"
      }
    },
    "Total Expenditure in foreign exchange": {
      "Current reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row13[0].NumericField141[0]",
      "Previous reporting period": "data[0].FormAOC4_Dtls[0].Segment2_2B[0].Table9[0].Row13[0].NumericField142[0]"
    }
  }


financial_parameter_profit_and_loss_mapping = {  
    "Proposed Dividend": {
      "Amount": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row1[0].NumericField143[0]",
      "Percentage": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row1[0].NumericField144[0]"
    },
    "Earnings per share (in Rupees)": {
      "Basic": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row2[0].NumericField145[0]",
      "Diluted": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row3[0].NumericField146[0]"
    },
    "Income in foreign currency": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row4[0].NumericField147[0]",
    "Expenditure in foreign currency": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row5[0].NumericField148[0]",
    "Revenue subsidies or grants received from government authority(ies)": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row6[0].NumericField149[0]",
    "Rent paid": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row7[0].NumericField150[0]",
    "Consumption of stores and spare parts": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row8[0].NumericField151[0]",
    "Gross value of transaction with related parties as per AS-18 (If applicable)": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row9[0].NumericField152[0]",
    "Bad debts of related parties as per AS-18 (If applicable)": "data[0].FormAOC4_Dtls[0].Segment2_3[0].Table12[0].Row10[0].NumericField153[0]"
  }
