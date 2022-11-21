from sqlalchemy.future import select
from sqlalchemy.orm import (declarative_base, relationship, Session)
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, create_engine, inspect,
                        func, Float)


Base = declarative_base()


class Cliente(Base):


    __tablename__ = "cliente"
    # atributos
    id = Column(Integer, primary_key = True)
    nome = Column(String)
    cpf = Column(String(11), nullable = False, unique = True)
    endereco = Column(String(50))

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}," \
               f" endereco={self.endereco}"


class Conta(Base):


    __tablename__ = "conta"
    id = Column(Integer, primary_key =  True)
    tipo = Column(String, nullable = False)
    agencia = Column(String, nullable = False)
    numero = Column(Integer, nullable = False)
    saldo = Column(Float, unique = True,  nullable = False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable = False)



    cliente = relationship(
        "Cliente", back_populates="conta"
    )


    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}," \
               f"numero={self.numero}, saldo={self.saldo})"

print(Cliente.__tablename__)
print(Conta.__tablename__)


# conexão com banco de dados
engine = create_engine("sqlite://")


# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)


# Investiga o esquema do banco de dados
insp = inspect(engine)
print(insp.has_table('cliente'))
print(insp.get_table_names())
print(insp.default_schema_name)

with Session(engine) as session:


    Mateus = Cliente(
        nome='Mateus',
        cpf='05967796584',
        endereco='Rua A- N12 - Malemba - Candeias/BA',
        conta=[Conta(tipo='Conta Poupança',
               agencia='14557',
               numero=121,
               saldo=1500.00)]
    )

    Gessica = Cliente(
        nome='Gessica',
        cpf='06687441236',
        endereco='Rua São Paulo- N91 - Santa Clara - Candeias/BA',
        conta=[Conta(tipo='Conta Corrente',
               agencia='18557',
               numero=845,
               saldo=2000.00)]
    )

    # Enviando para o banco de dados(persistencia de dados)
    session.add_all([Mateus, Gessica])
    session.commit()


stmt = select(Cliente).where(Cliente.nome.in_(["Mateus", "Gessica"]))
print("\nRecuperando clientes a partir de condição de filtragem\n")
for cliente in session.scalars(stmt):
    print(cliente)


stmt_conta = select(Conta).where(Conta.id_cliente.in_([2]))
print("\nRecuperando conta de Gessica\n")
for conta in session.scalars(stmt_conta):
    print(conta)

stmt_order = select(Cliente).order_by(Cliente.nome.desc())
print("\nRecuperando info de maneira ordenada\n")
for result in session.scalars(stmt_order):
    print(result)