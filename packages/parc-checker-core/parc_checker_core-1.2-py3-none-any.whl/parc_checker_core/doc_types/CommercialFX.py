from parc_checker_core import checkers
import json
from parc_checker_core.action import Action
from executor import task as tasks
from parc_checker_core.document_checker import DocumentChecker

DOC_TYPE = "CommercialFX"

def run(request, response, action):
    return DocumentTypeChecker(DOC_TYPE)(request, response, action)

class DocumentTypeChecker(DocumentChecker):

    def on_get(self, request, response):
        pass
    
    def on_create(self, request, response):
        pass

    def on_update(self, request, response):
        pass

    def on_delete(self, request, response):
        pass

    def on_change_cp(self, request, response):
        pass

    def on_list(self, request, response):
        pass

    def on_add(self, request, response):      
        VODB = request["VODB"]
        PRAWB351 = VODB["PRAWB351"]
        PRAWB352 = VODB["PRAWB352"][0]
        PRAWB354 = VODB["PRAWB354"][0]
        PRAWB355 = VODB["PRAWB355"]
        PRAWB355_1 = VODB["PRAWB355"][0]
        PRAWB355_2 = VODB["PRAWB355"][1]

        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PDID equeals to 5116GOB", checkers.getPropertyHasValueEqualsToChecker(PRAWB351, "PDID", "5116GOB")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check EFFECTIVEDATE is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB351, "EFFECTIVEDATE")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ENDDATE equeals to 9999-12-31", checkers.getPropertyHasValueEqualsToChecker(PRAWB351, "ENDDATE", "9999-12-31")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check AR_FORCE_YN equeals to N", checkers.getPropertyHasValueEqualsToChecker(PRAWB351, "AR_FORCE_YN", "N")))

        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB352 equals to non empty array", checkers.getPropertyHasNonEmptyArrayValueChecker(VODB, "PRAWB352")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB352 size equals 1", checkers.getPropertyArrayValueSizeChecker(VODB, "PRAWB352", 1)))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PARAMETERID equeals to FX-SALES-MARG", checkers.getPropertyHasValueEqualsToChecker(PRAWB352, "PARAMETERID", "FX-SALES-MARG")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PARM_FMT_TP equeals to TEXT", checkers.getPropertyHasValueEqualsToChecker(PRAWB352, "PARM_FMT_TP", "TEXT")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PARM_VAL_TX is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB352, "PARM_VAL_TX")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check AR_YN equeals to Y", checkers.getPropertyHasValueEqualsToChecker(PRAWB352, "AR_YN", "Y")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PD_CNTRL_YN equeals to Y", checkers.getPropertyHasValueEqualsToChecker(PRAWB352, "PD_CNTRL_YN", "Y")))

        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB354 equals to non empty array", checkers.getPropertyHasNonEmptyArrayValueChecker(VODB, "PRAWB354")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB354 size equals 1", checkers.getPropertyArrayValueSizeChecker(VODB, "PRAWB354", 1)))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check IPID is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB354, "IPID")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ARROLETYPE equeals to CUSTO", checkers.getPropertyHasValueEqualsToChecker(PRAWB354, "ARROLETYPE", "CUSTO")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check EFFECTIVEDATE is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB354, "EFFECTIVEDATE")))

        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB355 equals to non empty array", checkers.getPropertyHasNonEmptyArrayValueChecker(VODB, "PRAWB355")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check PRAWB355 size equals 2", checkers.getPropertyArrayValueSizeChecker(VODB, "PRAWB355", 2)))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ATTRTYPE equeals to ARLCS", checkers.getPropertyHasValueEqualsToChecker(PRAWB355_1, "ATTRTYPE", "ARLCS")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ATTRTEXT equeals to EFFEC", checkers.getPropertyHasValueEqualsToChecker(PRAWB355_1, "ATTRTEXT", "EFFEC")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check EFFECTIVEDATE is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB355_1, "EFFECTIVEDATE")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ATTRTYPE equeals to FCLST", checkers.getPropertyHasValueEqualsToChecker(PRAWB355_2, "ATTRTYPE", "FCLST")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check ATTRTEXT equeals to 1", checkers.getPropertyHasValueEqualsToChecker(PRAWB355_2, "ATTRTEXT", "1")))
        self.add_task(tasks.Task("CommercialFX - ADD - REQ - Check EFFECTIVEDATE is not empty", checkers.getPropertyHasNonEmptyValueChecker(PRAWB355_2, "EFFECTIVEDATE")))

    def on_param_update(self, request, response):
        pass

