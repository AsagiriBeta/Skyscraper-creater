package asagiribeta.skyscraper_creater.client

import net.fabricmc.fabric.api.datagen.v1.DataGeneratorEntrypoint
import net.fabricmc.fabric.api.datagen.v1.FabricDataGenerator

class Skyscraper_createrDataGenerator : DataGeneratorEntrypoint {

    override fun onInitializeDataGenerator(FabricDataGenerator fabricDataGenerator) {
        val pack = fabricDataGenerator.createPack();
    }
}
