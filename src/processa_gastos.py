from pyspark.sql import SparkSession
from pyspark.sql.functions import month, year, col, sum as spark_sum, avg, desc

# Inicializa a SparkSession
spark = SparkSession.builder \
    .appName("GastosPessoais") \
    .getOrCreate()


df = spark.read.csv("data/gastos_pessoais.csv", header=True, inferSchema=True)
df.show(10, truncate=False)
df.printSchema()
df = df.withColumn("mes", month(col("data")))
df = df.withColumn("ano", year(col("data")))

## GASTOS
total_gastos = df.agg(spark_sum("valor").alias("total_gastos")).collect()[0]["total_gastos"]
gastos_por_categoria = df.groupBy("categoria").agg(spark_sum("valor").alias("gasto_total")).orderBy(desc("gasto_total"))
gastos_por_categoria.show()
gastos_por_mes = df.groupBy("ano", "mes").agg(spark_sum("valor").alias("gasto_mes")).orderBy("ano", "mes")
gastos_por_mes.show()
top5 = df.orderBy(desc("valor")).select("data", "categoria", "valor", "descricao").limit(5)
top5.show()
media_categoria = df.groupBy("categoria").agg(avg("valor").alias("media_gasto")).orderBy(desc("media_gasto"))
media_categoria.show()
gastos_por_categoria.toPandas().to_csv('output/gastos_por_categoria.csv', index=False)
gastos_por_mes.toPandas().to_csv('output/gastos_por_mes.csv', index=False)
top5.toPandas().to_csv('output/top5_maiores_gastos.csv', index=False)
media_categoria.toPandas().to_csv('output/media_por_categoria.csv', index=False)
df.toPandas().to_csv('output/gastos_completo.csv', index=False)


print(f"Gasto total: R$ {total_gastos:.2f}")
