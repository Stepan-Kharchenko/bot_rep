import scripts.registration as reg
import scripts.admin as adm
import scripts.test as test

def bot_initialise(bot):
    Reg = reg.Reg
    reg.initialise(bot)
    Adm = adm.Admin
    adm.adm_initialise(bot)
    tst = test.Test
    test.initialise(bot)